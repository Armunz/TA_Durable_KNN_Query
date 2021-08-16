"""
QUERY PROCESSING
"""
import math
from Grid import *
import pickle
from threading import Thread, Lock
import copy

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


def collectCandidates(lock_candidates, lock_not_eligible, lock_future_candidates, 
sref_id, object_sref, position, timestamp, candidates, not_eligible_object, future_candidates, radius):
    
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
        elif timestamp < list_data[key]['time_in']:
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
                lock_future_candidates.acquire()
                future_candidates.append(eligible)
                lock_future_candidates.release()

def getObjectPosition(valid_sref, timestamp):
    for x in range(len(valid_sref['time_in'])):
        if timestamp in range(valid_sref['time_in'][x], valid_sref['time_out'][x]):
            return valid_sref['grid_positions'][x]

def getKNNCandidates(sref_id, valid_sref, k, timestamp, radius):
    candidates = []
    future_candidates = []
    object_sref = {}
    not_eligible_object = []
    
    sref_position = getObjectPosition(valid_sref, timestamp)
    list_data = grid.getListData(sref_position)
    
    if sref_id in list_data:
        object_sref = list_data[sref_id]

    lock_candidates = Lock()
    lock_not_eligible = Lock()
    lock_future_candidates = Lock()

    t = Thread(target=collectCandidates, args=(lock_candidates, lock_not_eligible, lock_future_candidates, sref_id,
    object_sref, sref_position, timestamp, candidates, not_eligible_object, future_candidates, radius))

    t.start()
    t.join()
    
    if len(candidates) >= k:
        return candidates, future_candidates

    else:
        previous_neighbor = []
        previous_neighbor.append(sref_position)
        level = 1
        while(level < grid.grid_size):
            neighbor_list = grid.getNeighborList(sref_position, level, previous_neighbor)
            if len(neighbor_list) == 0:
                break

            previous_neighbor.extend(neighbor_list)

            new_candidates = []
            new_not_eligible = []
            new_future_candidates = []

            thread_list = []
            for position in neighbor_list:
                t = Thread(target=collectCandidates, args=(lock_candidates, lock_not_eligible, lock_future_candidates,
                sref_id, object_sref, position, timestamp, new_candidates, new_not_eligible, new_future_candidates, radius))
                
                thread_list.append(t)
                t.start()

            for t in thread_list:
                t.join()
            
            candidates.extend(new_candidates)
            future_candidates.extend(new_future_candidates)    

            if len(candidates) < k:
                
                if len(not_eligible_object) != 0:
                    candidates.extend(not_eligible_object)
                

                else:
                    candidates.extend(new_not_eligible)

                not_eligible_object.clear()

                not_eligible_object.extend(new_not_eligible)
                
                if len(candidates) >= k:
                    not_eligible_object.clear()
                    break

            level += 1

        return candidates, future_candidates

def getKNNList(k, knn_candidates):
    result = []

    result = copy.deepcopy(knn_candidates)
    for object in result:
        object['delta_s'] = 1
    
    result = sorted(result, key = lambda i: i['distance'])
                
    return result[0:k]


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
        future_candidates = []
        sref_current_timestamp = {}

        t = tb
        while(t < tc):
            t_next = t + 1

            sref_current_timestamp = getCurrentTimestamp(valid_sref, t)
            if len(sref_current_timestamp) > 0:        
                knn_candidates, future_candidates = getKNNCandidates(sref, valid_sref, k, t, radius)
            else:
                if t_next < tc:
                    t = t_next
                    continue
                else:
                    break

            if len(knn_candidates) < k:
                if t_next < tc:
                    t = t_next
                    continue
                else:
                    break

            knn_list = getKNNList(k, knn_candidates)

            addToCS(CS, knn_list)
            t_sign = 0
            for time in range(t_next, tc):
                t_sign = time
                if time in range(sref_current_timestamp['time_in'], sref_current_timestamp['time_out']):

                    if isKNNObjectNotGone(knn_list, time, k) and not isCloserFutureCandidateComing( knn_list[len(knn_list) - 1], future_candidates, time):
                        addToCS(CS, knn_list)

                    elif not isKNNObjectNotGone(knn_list, time, k) and not isCloserFutureCandidateComing(knn_list[len(knn_list) - 1], future_candidates, time):
                        t = time
                        break
                    else:   
                        new_candidates = []

                        for object in knn_candidates:
                            if time in range(object['time_in'], object['time_out']):
                                new_candidates.append(object)

                        for object in future_candidates:
                            if time in range(object['time_in'], object['time_out']):
                                new_candidates.append(object)

                        knn_list = getKNNList(k, new_candidates)
                        addToCS(CS, knn_list)
                       
                    RS_id = getListId(RS)
                    for object in CS:
                        if object['id'] in RS_id:
                            continue
                        else:
                            if object['delta_s'] >= delta_min:
                                RS.append(object)
                      
                    CS = [x for x in CS if x not in RS]

                    if time > tc - delta_min:
                        cs_id = []
                        for object in CS:
                            if object['delta_s'] < delta_min - tc + time + 1:
                                cs_id.append(object['id'])
                        
                        CS = [x for x in CS if x['id'] not in cs_id]

                        if len(CS) == 0:
                            break
                        
                else:
                    t = time
                    break

            if len(CS) == 0 or t_sign == tc - 1:
                break

        return RS
    else:
        return "Error - Objek '{}' belum ada/telah hilang pada timestamp tersebut" .format(sref)

if __name__ == "__main__":
    grid = GridIndex
    object_timestamp_and_grid_pos = {}

    grid_file_name = 'grid.pickle'
    object_file_name = 'object_timestamp_and_grid_pos.pickle'

    with open(grid_file_name, 'rb') as file:
        grid = pickle.load(file)

    with open(object_file_name, 'rb') as file:
        object_timestamp_and_grid_pos = pickle.load(file)
    
    print("Durable K-NN Query Using Grid Index")
    print("Parameter: Objek Referensi (sref), Jumlah Objek yang Dicari (k), Interval Waktu Awal (tb), Interval Waktu Akhir (tc), Durability Threshold (r)\n")
    sref = input("Masukkan Objek Referensi (sref): ")
    k = input("Masukkan Jumlah Objek yang Ingin Dicari (k): ")
    tb = input("Masukkan Interval Waktu Awal (tb): ")
    tc = input("Masukkan Interval Waktu Akhir (tc): ")
    r = input("Masukkan Durability Threshold (0 - 100): ")
    print("Loading...")
    result = dknnQuery(sref, int(k), int(tb), int(tc), int(r))
    print("Objek Hasil (RS): ", result)
    print("Jumlah Objek Hasil (RS): ", len(result))