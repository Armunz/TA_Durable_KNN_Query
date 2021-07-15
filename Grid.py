"""
CLASS GRID INDEX
"""
import itertools

class GridIndex:
    def __init__(self, grid_size, dimensions, max_value):
        self.grid_size = grid_size
        self.dimensions = dimensions
        self.grid_length = max_value / grid_size
        self.amount_data = None
        self.grid = {}
        for i in range(grid_size ** dimensions):
            grid_key = 'G' + str(i)
            self.grid[grid_key] = {}
            self.grid[grid_key]['positions'] = []
            self.grid[grid_key]['list_data'] = {}
            self.grid[grid_key]['is_empty'] = True
            
            temp_position = i
            for axis in range(dimensions):
                axis_position = temp_position % grid_size
                self.grid[grid_key]['positions'].append(axis_position)
                temp_position //= grid_size

    def getAmountData(self):
        return self.amount_data

    def printGrid(self):
        print(self.grid)

    def addDataObject(self, list_data_object):
        if list_data_object is None or len(list_data_object) == 0:
            print("Data Kosong")
        else:
            self.amount_data = len(list_data_object)
            for data in list_data_object:
                object_loc = []
                for axis in range(self.dimensions):
                    object_loc.append(data['values'][axis] // self.grid_length)
                for key in self.grid.keys():
                    if self.grid[key]['positions'] == object_loc:
                        id = data['id']
                        self.grid[key]['list_data'][id] = {}
                        self.grid[key]['list_data'][id]['values'] = data['values']
                        self.grid[key]['list_data'][id]['time_in'] = data['time_in']
                        self.grid[key]['list_data'][id]['time_out'] = data['time_out']
                        self.grid[key]['list_data'][id]['grid_positions'] = self.grid[key]['positions']
                        self.grid[key]['is_empty'] = False
    
    def getGridPosition(self, object_id):
        position_list = []
        for key in self.grid.keys():
            if object_id in self.grid[key]['list_data']:
                position_list.append(self.grid[key]['list_data'][object_id]['grid_positions'])
        return position_list

    def getDataTimeIn(self, object_id):
        timestamp_list = []
        for key in self.grid.keys():
            if object_id in self.grid[key]['list_data']:
                timestamp_list.append(self.grid[key]['list_data'][object_id]['time_in'])
        return timestamp_list

    def getDataTimeOut(self, object_id):
        timestamp_list = []
        for key in self.grid.keys():
            if object_id in self.grid[key]['list_data']:
                timestamp_list.append(self.grid[key]['list_data'][object_id]['time_out'])
        return timestamp_list

    def getListData(self, position):
        for key in self.grid.keys():
            if position == self.grid[key]['positions']:
                return self.grid[key]['list_data']

    def isValidNeighbor(self, position):
        counter = 0
        for index in range(self.dimensions):
            if(position[index] >= 0 and position[index] < self.grid_size):
                counter += 1        
        if(counter == self.dimensions):
            counter = 0
            return True
 
        return False

    def getNeighborList(self, grid_position, level, previous_neighbor):
        valid_neighbor_list = []
        iterators = []

        lower_bound = level * -1
        upper_bound = level + 1

        for x in range(lower_bound, upper_bound):
            iterators.append(x)
        
        neighbors_direction = itertools.product(iterators, repeat=self.dimensions)
        neighbors_direction = list(neighbors_direction)
        neighbor_candidates = []

        for item in neighbors_direction:
            direction = list(item)
            neighbor = []
            for i in range(len(direction)):
                neighbor.append(grid_position[i] + direction[i])
            neighbor_candidates.append(neighbor)
        
        neighbor_candidates = [x for x in neighbor_candidates if x not in previous_neighbor]

        for item in neighbor_candidates:
            if self.isValidNeighbor(item):
                valid_neighbor_list.append(item)
        
        return valid_neighbor_list
    