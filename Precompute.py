"""
DATA PRECOMPUTING
"""
import csv
import pickle
from Grid import *
import time

def loadDataFromCSV(file_name):
    list_object_data = []
    list_x_value = []
    list_y_value = []
    list_z_value = []

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                list_object_data.append({
                    'id': row[0],
                    'values': [int(row[1]), int(row[2]), int(row[3])],
                    'time_in': int(row[4]),
                    'time_out': int(row[5])
                })
                list_x_value.append(int(row[1]))
                list_y_value.append(int(row[2]))
                list_z_value.append(int(row[3]))
            line_count += 1
    
    return list_object_data, list_x_value, list_y_value, list_z_value

def getLargestPoint(list_x_value, list_y_value, list_z_value):
    list_x_value = sorted(list_x_value)
    list_y_value = sorted(list_y_value)
    list_z_value = sorted(list_z_value)
    largest_x = list_x_value.pop()
    largest_y = list_y_value.pop()
    largest_z = list_z_value.pop()

    return largest_x, largest_y, largest_z

def getDimension(list_object_data):
    first_object = list_object_data[0]
    dimension = len(first_object['values'])
    
    return dimension


def getMaxValue(largest_x, largest_y, largest_z, size):
    list_value = []
    list_value.append(largest_x)
    list_value.append(largest_y)
    list_value.append(largest_z)
    sorted_value = sorted(list_value)
    max_value = sorted_value.pop()
    mod_10 = max_value % size
    if mod_10 == 0:
        return max_value

    max_value += abs(mod_10 - size)
    return max_value

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

if __name__ == "__main__":
    print("Precomputing...")
    list_object_data, list_x_value, list_y_value, list_z_value = loadDataFromCSV('random_data_3d.csv')
    largest_x, largest_y, largest_z = getLargestPoint(list_x_value, list_y_value, list_z_value)
    
    dimension = getDimension(list_object_data)
    max_value = getMaxValue(largest_x, largest_y, largest_z, 10)
    
    grid = makeGrid(10, dimension, max_value, list_object_data)
    
    object_data_timestamp_and_grid_pos = makeObjectDataTimestampAndGridPosition(list_object_data, grid)

    grid_file_name = 'grid.pickle'
    object_file_name = 'object_timestamp_and_grid_pos.pickle'

    dumpGrid(grid, grid_file_name)
    dumpObjectTimestampAndGridPosition(object_data_timestamp_and_grid_pos, object_file_name)