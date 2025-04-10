import lzma
import xml.etree.ElementTree as ET
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from block_data import BLOCK_SHAPES, ROTATION_OFFSET

MAX_LEVEL_SIZE = (110,80)

DEATH_PIT_OFFSET = 5
CEILING_OFFSET = -5
LEFT_WALL_OFFSET = 5
RIGHT_WALL_OFFSET = -5

X_OFFSET = 54
Y_OFFSET = 39

class FileParser():
    def __init__(self):
        self.tree = None
        self.root = None
    
    def parse_file(self, file_path):
        with lzma.open(file_path, 'rt', encoding='utf-8') as file:
            tree = ET.parse(file)
            root = tree.getroot()
            
    
        map_data = self.get_color_grids(root)
        map_data['color_dict'] = self.reverse_color_dict(map_data['color_dict'])
        print(map_data['config'])
        print(map_data['unopt_blocks'])
        
        return map_data
    
    def reverse_color_dict(self, color_dict):
        reversed_dict = {v: list(k) for k, v in color_dict.items()}
        return reversed_dict
        
    def get_level_boundaries(self, root):
        boundaries = {}
        
        for child in root:
            if child.tag == 'moved':
                block = child.attrib
                if block['path'] == "DeathPit":
                    print(block['path'], block['pY'])
                    boundaries['down'] = int(block['pY']) + DEATH_PIT_OFFSET
                if block['path'] == "LeftWall":
                    boundaries['left'] = int(block['pX']) + LEFT_WALL_OFFSET
                if block['path'] == "RightWall":
                    boundaries['right'] = int(block['pX']) + RIGHT_WALL_OFFSET
                if block['path'] == "Ceiling":
                    boundaries['up'] = int(block['pY']) + CEILING_OFFSET
        return boundaries
            
    def create_block_array(self, boundaries):
        num_cols = (boundaries['right'] - boundaries['left']) + 1
        num_rows = (boundaries['up'] - boundaries['down']) + 1
        block_array = np.zeros((num_rows, num_cols))
        return block_array
    
    def get_color_grids(self, root):
        color_to_points = {}
        color_dict = {}
        points = []
        optimizable_blocks = BLOCK_SHAPES.keys()
        unoptimizable_blocks = []
        map_config = []
        for child in root:
            if child.tag == 'block':
                block = child.attrib
                blockID = int(child.attrib['blockID'])
                pX = float(block['pX'])
                pY = float(block['pY'])
                
                if blockID in optimizable_blocks:
                    if 'colR' in block:
                        color = (
                            block['colR'], 
                            block['colG'],
                            block['colB']
                            )
                        used_colors = color_dict.keys()
                        if color not in used_colors:
                            color_dict[color] = len(used_colors) + 1
                    block_data = BLOCK_SHAPES[blockID]
                    rotation = int(block['rZ'])
                    if blockID == 44:
                        rotation = (rotation + 180) % 360
                    if rotation == 0 or rotation == 180:
                        width = block_data['width']
                        height = block_data['height']
                    else:
                        width = block_data['height']
                        height = block_data['width']
                    if width % 2 == 1:
                        x_offset = math.floor((width/2))
                    else:
                        x_offset = (width/2) + ROTATION_OFFSET[rotation]['x']
                    if height % 2 == 1:
                        y_offset = math.floor((height/2))
                    else:
                        y_offset = (height/2) + ROTATION_OFFSET[rotation]['y']
                    
                    x_pos = pX - x_offset
                    y_pos = pY - y_offset
                    
                    for x in range(width):
                        for y in range(height):
                            point = (x_pos + x, y_pos + y)
                            color_to_points.setdefault(color, []).append(point)
                else:
                    unoptimizable_blocks.append(child)
            else:
                map_config.append(child)
                            
        grid = np.zeros((MAX_LEVEL_SIZE[1], MAX_LEVEL_SIZE[0]), dtype=int)
        
        for color, points in color_to_points.items():
            for x,y in points:
                xi = int(round(x)) + X_OFFSET
                yi = int(round(y)) + Y_OFFSET
                if 0 <= xi < MAX_LEVEL_SIZE[0] and 0 <= yi < MAX_LEVEL_SIZE[1]:
                    grid[yi, xi] = color_dict[color]
        self.plot_matrix(grid)
        padded_grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
        self.plot_matrix(padded_grid)
        
        scene_data = root.attrib
        map_data = {
            'grid': padded_grid,
            'color_dict': color_dict,
            'unopt_blocks': unoptimizable_blocks,
            'config': map_config,
            'scene_data': scene_data
        }
        return map_data
                
    def plot_matrix(self, arr):
        # colours_float = {key: [float(val) for val in value] for key, value in self.colour_dict.items()}
        # cmap = ListedColormap(colours_float.values())
        plt.imshow(arr)
        plt.gca().invert_yaxis()
        plt.show()

if __name__ == "__main__":
    file_path = 'testfile2.c.snapshot'
    fp = FileParser()
    fp.parse_file(file_path)
    
