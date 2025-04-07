import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random

from shape_optimizer import ShapeOptimizer

class BlockOptimizer():
    def __init__(self):
        pass
    
    def plot_matrix(self, arr):
        # colours_float = {key: [float(val) for val in value] for key, value in self.colour_dict.items()}
        # cmap = ListedColormap(colours_float.values())
        plt.imshow(arr)
        plt.gca().invert_yaxis()
        plt.show()
    
    def optimize_level(self, map_data):
        start_time = time.time()
        grid = map_data['grid']
        color_dict = map_data['color_dict']
        block_list = []
        for color in color_dict.keys():
            shape_list = self.find_shapes(grid, color)
            for shape in shape_list:
                tmp_arr = grid.copy()
                so = ShapeOptimizer()
                block_list.extend(so.optimize_shape(shape, tmp_arr, color))
        print(f"Runtime: {time.time() - start_time} seconds")
        return block_list
        
    def find_shapes(self, grid, color):
        shape_list = []
        arr_rows = np.size(grid,0)
        arr_cols = np.size(grid,1)
        tmp_arr = np.copy(grid)
        for col in range(arr_cols):
            for row in range(arr_rows):
                if tmp_arr[row,col] == color:
                    shape_list.append(self.produce_shape(tmp_arr, (row,col), color))
        return shape_list
                    
    def produce_shape(self, arr, position, color):
        shape = [position]
        queue = [position]
        visited = set() 
        visited.add(position)
        
        while queue:
            current_position = queue.pop(0)
            adjacent_tiles = [
                (current_position[0] + 1, current_position[1]), 
                (current_position[0] - 1, current_position[1]), 
                (current_position[0], current_position[1] + 1), 
                (current_position[0], current_position[1] - 1)
            ]
            
            for tile in adjacent_tiles:
                if not tile in visited:
                    if tile[0] >= 0 and tile[1] >= 0 and tile[0] < arr.shape[0] and tile[1] < arr.shape[1]:  
                        if arr[tile] == color:
                            queue.append(tile)
                            shape.append(tile)
                            visited.add(tile)
        for pos in shape:
            arr[pos] = 0
        return shape
    
if __name__=="__main__":
    arr_size = (5, 5)
    print(f"Size: {arr_size}")
    test_arr = np.ones(arr_size)
    # test_arr = np.random.randint(0, 2, size=arr_size)
    padded_grid = np.pad(test_arr, pad_width=3, mode='constant', constant_values=0)
    bo = BlockOptimizer()
    color_dict = {
        1 : ['0', '0', '0']
    }
    unoptimizable_blocks = []
    map_config = []
    scene_data = []
    map_data = {
        'grid': padded_grid,
        'color_dict': color_dict,
        'unopt_blocks': unoptimizable_blocks,
        'config': map_config,
        'scene_data': scene_data
    }
    bo.optimize_level(map_data)
    
    
