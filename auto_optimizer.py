import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class AutoOptimizer:
    def __init__(self,arr, colour_dict):
        self.arr = arr
        self.current_colour = 1
        self.shape_list = []
        self.block_shapes = [ #[x,y,blockID,offsetX,offsetY,rz]
            [1,1,40,0,0,0],
            [2,1,41,0,0,0],
            [1,2,41,0,1,270],
            [3,1,42,1,0,0],
            [1,3,42,0,1,270],
            [4,1,43,1,0,0],
            [1,4,43,0,2,270],
            [8,1,44,4,0,0],
            [1,8,44,0,3,270],
            [16,1,45,7,0,0],
            [1,16,45,0,8,270],
            [2,2,47,0,1,0],
            [2,4,46,1,2,270],
            [4,2,46,1,1,0],
            [4,4,48,1,2,0],
            [8,8,49,3,4,0],
            [6,16,50,2,8,0],
            [16,6,50,8,3,270]
        ]
        self.block_list = []
        self.colour_dict = colour_dict
        
        self.Optimize_Level()
            
    def Plot_Matrix(self, arr):
        # colours_float = {key: [float(val) for val in value] for key, value in self.colour_dict.items()}
        # cmap = ListedColormap(colours_float.values())
        plt.imshow(arr)
        plt.gca().invert_yaxis()
        plt.show()
        
    def Optimize_Level(self):
        for colour in self.colour_dict.keys():
            print('h', colour, self.colour_dict[colour], 'finding_shapes')
            self.current_colour = colour
            self.shape_list = []
            self.Find_Shapes(colour)
            print(len(self.shape_list))
            
            for shape in self.shape_list:
                if len(shape) <= 25:
                    self.Full_Optimize_Shape(shape)
                else:
                    self.Optimize_Shape(shape)
        self.Plot_Matrix(self.arr)
            
    def Find_Shapes(self, colour):
        arr_rows = np.size(self.arr,0)
        arr_cols = np.size(self.arr,1)
        tmp_arr = np.copy(self.arr)
        for col in range(arr_cols):
            for row in range(arr_rows):
                if tmp_arr[row,col] == colour:
                    self.shape_list.append((self.Produce_Shape(tmp_arr, (row,col))))

    def Produce_Shape(self, arr, position):
        shape = [position]
        queue = [position]
        visited = set()  # Create a set to keep track of visited positions
        visited.add(position)  # Mark the initial position as visited
        
        while queue:
            current_position = queue.pop(0)
            adjacent_tiles = [
                (current_position[0] + 1, current_position[1]), 
                (current_position[0] - 1, current_position[1]), 
                (current_position[0], current_position[1] + 1), 
                (current_position[0], current_position[1] - 1)
            ]
            
            for tile in adjacent_tiles:
                if tile[0] >= 0 and tile[1] >= 0 and tile[0] < arr.shape[0] and tile[1] < arr.shape[1]:  # Check boundaries
                    if arr[tile] == self.current_colour and tile not in visited:
                        queue.append(tile)
                        shape.append(tile)
                        visited.add(tile)  # Mark this tile as visited
        for pos in shape:
            arr[pos] = 0
        return shape
        
    def Crop_Shape(self, shape):
        min_x = min([coord[1] for coord in shape])
        max_x = max([coord[1] for coord in shape])
        min_y = min([coord[0] for coord in shape])
        max_y = max([coord[0] for coord in shape])

        return [min_x, max_x, min_y, max_y]
        
    def Optimize_Shape(self, shape):
        fitting_blocks = []
        full_positions = []
        crop = self.Crop_Shape(shape)
        for block in self.block_shapes:
            if block[1] <= (crop[3] - crop[2] + 1) and block[0] <= (crop[1] - crop[0] + 1):
                fitting_blocks.insert(0,block)

        for block in fitting_blocks:
            shape = [position for position in shape if position not in full_positions]
            full_positions.extend(self.Fit_Block(shape, block))

    def Fit_Block(self, shape, block):
        full_positions = []
        for position in shape:
            if np.all(self.arr[position[0]:position[0]+block[1],position[1]:position[1]+block[0]] == self.current_colour):
                self.block_list.append([position[1],position[0],block[2],block[3],block[4],block[5], self.current_colour])
                self.arr[position[0]:position[0]+block[1],position[1]:position[1]+block[0]] = block[2]
                full_positions.extend([pos for pos in shape if position[0] <= pos[0] <= position[0]+block[1] - 1 and position[1] <= pos[1] <= position[1]+block[0] - 1])
        return full_positions

if __name__ == "__main__":
    pass

