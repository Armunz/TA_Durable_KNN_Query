"""
DATA PRECOMPUTING
"""
import csv
import pickle
from Grid import *
import time

def loadDataFromCSV(file_name):
    list_object_data = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_column_names = []
        for row in csv_reader:
            list_of_column_names.extend(row)
            break
        # 2 Dimensi
        if len(list_of_column_names) == 5:
            for row in csv_reader:
                list_object_data.append({
                    'id': row[0],
                    'values': [float(row[1]), float(row[2])],
                    'time_in': int(row[3]),
                    'time_out': int(row[4])
                })
                
        # 3 Dimensi        
        elif len(list_of_column_names) == 6:
            for row in csv_reader:
                list_object_data.append({
                    'id': row[0],
                    'values': [float(row[1]), float(row[2]), float(row[3])],
                    'time_in': int(row[4]),
                    'time_out': int(row[5])
                })

    return list_object_data

def getDimension(list_object_data):
    first_object = list_object_data[0]
    dimension = len(first_object['values'])
    
    return dimension


def makeGrid(size, dimension, max_value, list_object_data):
    grid = GridIndex(size, dimension, max_value)
    grid.addDataObject(list_object_data)

    return grid

def makeObjectDataTimestampAndGridPosition(list_object_data, grid):
    object_data = {}

    for data in list_object_data:
        id = data['id']
        object_data[id] = {}
        object_data[id]['time_in'] = grid.getDataTimeIn(id)
        object_data[id]['time_out'] = grid.getDataTimeOut(id)
        object_data[id]['grid_positions'] = grid.getGridPosition(id)

    return object_data

def dumpGrid(grid, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(grid, file)

def dumpObjectTimestampAndGridPosition(object, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(object, file)

def runPrecompute(grid_size ,file_name):
    list_object_data = loadDataFromCSV(file_name)
    dimension = getDimension(list_object_data)
    max_value = 1
    grid = makeGrid(int(grid_size), dimension, max_value, list_object_data)
    object_data_timestamp_and_grid_pos = makeObjectDataTimestampAndGridPosition(list_object_data, grid)
    
    grid_file_name = 'grid.pickle'
    object_file_name = 'object_timestamp_and_grid_pos.pickle'

    dumpGrid(grid, grid_file_name)
    dumpObjectTimestampAndGridPosition(object_data_timestamp_and_grid_pos, object_file_name)

if __name__ == "__main__":
    print("Precomputing...")
    grid_size = input("Masukkan size dari Grid:")
    
    print("Dataset yang Tersedia:")
    print("1. IND")
    print("2. ANT")
    print("3. FC")
    dataset_choice = input("Pilih Jenis Dataset: ")

    file_name = None
    if dataset_choice == '1':
        print("Berkas yang Tersedia:")
        print("=== 2 Dimensi ===")
        print("1. random_10000_2d_ind.csv")
        print("2. random_30000_2d_ind.csv")
        print("3. random_50000_2d_ind.csv")
        print("4. random_100000_2d_ind.csv")
        print("5. random_200000_2d_ind.csv")
        print("6. random_300000_2d_ind.csv")
        print("=== 3 Dimensi ===")
        print("7. random_50000_3d_ind.csv")
        file_choice = input("Pilih Berkas yang Tersedia:")
        if file_choice == '1':
            file_name = "random_10000_2d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '2':
            file_name = "random_30000_2d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '3':
            file_name = "random_50000_2d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '4':
            file_name = "random_100000_2d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '5':
            file_name = "random_200000_2d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '6':
            file_name = "random_300000_2d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '7':
            file_name = "random_50000_3d_ind.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        else:
            print("File Tidak Valid")
    elif dataset_choice == '2':
        print("Berkas yang Tersedia:")
        print("=== 2 Dimensi ===")
        print("1. random_10000_2d_ant.csv")
        print("2. random_30000_2d_ant.csv")
        print("3. random_50000_2d_ant.csv")
        print("4. random_100000_2d_ant.csv")
        print("5. random_200000_2d_ant.csv")
        print("6. random_300000_2d_ant.csv")
        print("=== 3 Dimensi ===")
        print("7. random_50000_3d_ant.csv")
        file_choice = input("Pilih Berkas yang Tersedia:")
        if file_choice == '1':
            file_name = "random_10000_2d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '2':
            file_name = "random_30000_2d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '3':
            file_name = "random_50000_2d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '4':
            file_name = "random_100000_2d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '5':
            file_name = "random_200000_2d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '6':
            file_name = "random_300000_2d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '7':
            file_name = "random_50000_3d_ant.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        else:
            print("File Tidak Valid")
    elif dataset_choice == '3':
        print("Berkas yang Tersedia:")
        print("=== 2 Dimensi ===")
        print("1. random_10000_2d_fc.csv")
        print("2. random_30000_2d_fc.csv")
        print("3. random_50000_2d_fc.csv")
        print("4. random_100000_2d_fc.csv")
        print("5. random_200000_2d_fc.csv")
        print("6. random_300000_2d_fc.csv")
        print("=== 3 Dimensi ===")
        print("7. random_50000_3d_fc.csv")
        file_choice = input("Pilih Berkas yang Tersedia:")
        if file_choice == '1':
            file_name = "random_10000_2d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '2':
            file_name = "random_30000_2d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '3':
            file_name = "random_50000_2d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '4':
            file_name = "random_100000_2d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '5':
            file_name = "random_200000_2d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '6':
            file_name = "random_300000_2d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        elif file_choice == '7':
            file_name = "random_50000_3d_fc.csv"
            start = time.time()
            runPrecompute(grid_size, file_name)
            print("--- Execution Time: %s seconds ---" % (time.time() - start))
        else:
            print("File Tidak Valid")
    else:
        print("Dataset Tidak Valid")