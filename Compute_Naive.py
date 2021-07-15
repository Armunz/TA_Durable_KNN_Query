import math
from Grid import *
import pickle
from threading import Thread, Lock
import copy
import time
import tracemalloc

def checkObjectValidity(object_id, tb, tc):
    if object_id not in object_timestamp_and_grid_pos.keys():
        return False, None
    
    time_in = sorted(object_timestamp_and_grid_pos[object_id]['time_in'])
    time_out = sorted(object_timestamp_and_grid_pos[object_id]['time_out'], reverse=True)

    if tb < time_in[0] or tc > time_out[0] - 1:
        return False, None
    return True, object_timestamp_and_grid_pos[object_id]


def getCurrentTimestamp(valid_sref, timestamp):
    current_timestamp = {}
    for x in range(len(valid_sref['time_in'])):
        if timestamp in range(valid_sref['time_in'][x], valid_sref['time_out'][x]):
            current_timestamp = {
                'time_in': valid_sref['time_in'][x],
                'time_out': valid_sref['time_out'][x]
            } 
            return current_timestamp
    return current_timestamp


def collectCandidates(lock_candidates, lock_not_eligible, 
sref_id, object_sref, position, timestamp, candidates, not_eligible_object, radius):
    
    list_data = grid.getListData(position)
    for key in list_data.keys():
        if key == sref_id:
            continue
        if timestamp in range(list_data[key]['time_in'], list_data[key]['time_out']):
            delta = []
            for x in range(len(object_sref['values'])):
                delta.append(object_sref['values'][x] - list_data[key]['values'][x])

            delta_result = []
            for element in delta:
                element *= element
                delta_result.append(element)

            delta_result = sum(delta_result)
            
            distance = math.sqrt(delta_result) 
            # print("Distance: ", distance)
            if distance <= radius:
                eligible = {
                    'id': key,
                    'values': list_data[key]['values'],
                    'time_in': list_data[key]['time_in'],
                    'time_out': list_data[key]['time_out'],
                    'grid_positions': list_data[key]['grid_positions'],
                    'distance': distance
                }
                lock_candidates.acquire()
                candidates.append(eligible)
                lock_candidates.release()
            else:
                not_eligible = {
                    'id': key,
                    'values': list_data[key]['values'],
                    'time_in': list_data[key]['time_in'],
                    'time_out': list_data[key]['time_out'],
                    'grid_positions': list_data[key]['grid_positions'],
                    'distance': distance
                }
                lock_not_eligible.acquire()
                not_eligible_object.append(not_eligible)
                lock_not_eligible.release()

def getObjectPosition(valid_sref, timestamp):
    for x in range(len(valid_sref['time_in'])):
        if timestamp in range(valid_sref['time_in'][x], valid_sref['time_out'][x]):
            return valid_sref['grid_positions'][x]

def getKNNCandidates(sref_id, valid_sref, k, timestamp, radius):
    candidates = []
    object_sref = {}
    not_eligible_object = []
    
    sref_position = getObjectPosition(valid_sref, timestamp)
    list_data = grid.getListData(sref_position)
    
    # for key in list_data.keys():
    #     if key == sref_id:
    #         object_sref = list_data[key]
    if sref_id in list_data:
        object_sref = list_data[sref_id]

    lock_candidates = Lock()
    lock_not_eligible = Lock()

    # Find data in its grid cell first
    t = Thread(target=collectCandidates, args=(lock_candidates, lock_not_eligible, sref_id,
    object_sref, sref_position, timestamp, candidates, not_eligible_object, radius))

    t.start()
    t.join()
    
    if len(candidates) >= k:
        return candidates

    else:
        # Find data at it's grid cell neighbor
        previous_neighbor = []
        previous_neighbor.append(sref_position)
        level = 1
        # print("Grid Size: ", grid.grid_size)
        while(level < grid.grid_size):
            neighbor_list = grid.getNeighborList(sref_position, level, previous_neighbor)
            # print("Neighbor List level {}: {}" .format(level, neighbor_list))
            if len(neighbor_list) == 0:
                # print("Masuk sini?")
                break

            previous_neighbor.extend(neighbor_list)

            new_candidates = []
            new_not_eligible = []

            thread_list = []
            for position in neighbor_list:
                t = Thread(target=collectCandidates, args=(lock_candidates, lock_not_eligible,
                sref_id, object_sref, position, timestamp, new_candidates, new_not_eligible, radius))
                
                thread_list.append(t)
                t.start()

            for t in thread_list:
                t.join()
            
            candidates.extend(new_candidates) 

            # print("Candidates level {}: {}" .format(level, candidates))
            # print("Not eligible level {}: {}" .format(level, new_not_eligible))
            # print("Future Candidates level {}: {}" .format(level, future_candidates))

            if len(candidates) < k:
                
                if len(not_eligible_object) != 0:
                    candidates.extend(not_eligible_object)
                

                else:
                    candidates.extend(new_not_eligible)

                not_eligible_object.clear()

                not_eligible_object.extend(new_not_eligible)
                
                if len(candidates) >= k:
                    # print("Apakah Masuk sini?")
                    not_eligible_object.clear()
                    break

            level += 1

        return candidates

def getKNNList(k, knn_candidates):
    result = []

    result = copy.deepcopy(knn_candidates)
    for object in result:
        object['delta_s'] = 1
    
    result = sorted(result, key = lambda i: i['distance'])
                
    return result[0:k]


def addToCS(CS, knn_list):
    if len(CS) == 0:
        CS.extend(knn_list)
    else:
        new_nn_list = []
        id_list = []
        for object in CS:
            id_list.append(object['id'])

        for i in knn_list:
            if i['id'] not in id_list:
                new_nn_list.append(i)
            for object in CS:
                if i['id'] == object['id']:
                    object['delta_s'] += 1

        if len(new_nn_list) != 0:
            CS.extend(new_nn_list)

def getListId(object_list):
    list_id = []
    for object in object_list:
        list_id.append(object['id'])
    return list_id

def isKNNObjectNotGone(knn_list, timestamp, k):
    counter = 0
    for object in knn_list:
        if timestamp in range(object['time_in'], object['time_out']):
            counter += 1
             
    if counter == k:
        return True
    return False

def isCloserFutureCandidateComing(last_knn_object, future_candidates, timestamp):
    for object in future_candidates:
        if timestamp in range(object['time_in'], object['time_out']):
            if object['distance'] < last_knn_object['distance']:
                return True
    return False

def dknnQuery(sref, k, tb, tc, r):
    data_length = grid.getAmountData()
    isValidTimestamp, valid_sref = checkObjectValidity(sref, tb, tc)
    if k > data_length - 1:
        return "Error - Nilai k melebihi jumlah seluruh objek"
    if tb >= tc:
        return "Error - Timestamp tidak valid"
    if valid_sref is None:
        return "Error - Objek tidak valid"
    if isValidTimestamp:
        r *= 0.01
        delta_min = math.ceil(r * (tc - tb))
        radius = math.sqrt( k / math.pi * data_length)
        CS = []
        RS = []
        knn_list = []
        knn_candidates = []
        sref_current_timestamp = {}
        t = tb

        while(t < tc):
            # print("Iterasi While: ", t)
            t_next = t + 1

            sref_current_timestamp = getCurrentTimestamp(valid_sref, t)
            if len(sref_current_timestamp) > 0:        
                knn_candidates = getKNNCandidates(sref, valid_sref, k, t, radius)
            else:
                if t_next < tc:
                    t = t_next
                    continue
                else:
                    break

            # Jika kandidat tidak memenuhi jumlah k, maka cari kandidat di timestamp selanjutnya
            if len(knn_candidates) < k:
                if t_next < tc:
                    t = t_next
                    continue
                else:
                    break
            # print("Candidates at timestamp {}: {}" .format(t, knn_candidates))
            # Get KNN List
            knn_list = getKNNList(k, knn_candidates)
            # print("KNN ketika timestamp {}: {}" .format(t, knn_list))
            # Append to CS
            addToCS(CS, knn_list)
            # print("CS ketika timestamp {}: {}" .format(t, CS))
            
            # Move CS to RS
            RS_id = getListId(RS)
            for object in CS:
                if object['id'] in RS_id:
                    continue
                else:
                    if object['delta_s'] >= delta_min:
                        RS.append(object)
                
            CS = [x for x in CS if x not in RS]
            # print("CS After move to RS: ", CS)
            # print("RS: ", RS)

            # Jika object di CS tidak mungkin menjadi hasil
            if t > tc - delta_min:
                cs_id = []
                for object in CS:
                    if object['delta_s'] < delta_min - tc + t_next:
                        cs_id.append(object['id'])
                
                CS = [x for x in CS if x['id'] not in cs_id]
                # print("CS Now: ", CS)
                if len(CS) == 0:
                    break
  
            t = t_next

        return RS
    else:
        return "Error - Objek '{}' belum ada/telah hilang pada timestamp tersebut" .format(sref)

if __name__ == "__main__":
    # start = time.time()
    tracemalloc.start()
    grid = GridIndex
    object_timestamp_and_grid_pos = {}

    grid_file_name = 'grid.pickle'
    object_file_name = 'object_timestamp_and_grid_pos.pickle'

    with open(grid_file_name, 'rb') as file:
        grid = pickle.load(file)

    with open(object_file_name, 'rb') as file:
        object_timestamp_and_grid_pos = pickle.load(file)

    # print(len(object_timestamp_and_grid_pos))
    result = dknnQuery('qdevyurm', 50, 618, 718, 70)
    # print("RS: ", result)
    # print("RS Length: ", len(result))
    # for object in result:
    #     print(object['id'])
    # print("--- Execution Time: %s seconds ---" % (time.time() - start))
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6} MB; Peak was {peak / 10**6} MB")
    tracemalloc.stop()
