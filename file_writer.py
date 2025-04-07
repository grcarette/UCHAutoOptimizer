import xml.etree.ElementTree as ET
import random
import numpy as np
import math
import lzma
import json
import os

from block_data import BLOCK_SHAPES, ROTATION_OFFSET

class SnapshotCreator:
    def __init__(self, block_list, map_data, filepath):
        self.map_data = map_data   
        self.base_filepath = filepath
        self.block_list = block_list
        self.block_count = 7
        self.center_x = 0
        self.center_y = 1
        self.pitleft_offset = 4
        self.ceilright_offset = 3
        self.start_offset = -0.5
        self.max_level_size = [88,110]
        self.boundaries = [np.size(map_data['grid'], 1), np.size(map_data['grid'], 0)]
        self.offset_x = self.center_x - math.floor(self.boundaries[0]/2)
        self.offset_y = self.center_y - math.floor(self.boundaries[1]/2)
        
        self.color_dict = map_data['color_dict']
        
        self.Generate_Level()
        
    def Generate_Level(self):
        root = self.Create_Scene()
        root = self.Add_Blocks(root)
        self.Write_To_File(root)

    def Create_Scene(self):
        root = ET.Element("scene", self.map_data['scene_data'])
        for element in self.map_data['config']:
            root.append(element)
        # for element in self.map_data['unopt_blocks']:
        #     root.append(element)
        return root
        
    def Create_Block(self,scene, x_pos,y_pos,blockID,block_offset_x, block_offset_y,rotation,color,xscale=1):
        block = ET.SubElement(scene, "block")
        
        pos_x = x_pos+self.offset_x+block_offset_x
        pos_y = y_pos+self.offset_y+block_offset_y
        
        block.set("sceneID", f"{self.block_count}")
        block.set("blockID",f"{blockID}")
        block.set("pX",f"{pos_x}")
        block.set("pY",f"{pos_y}")
        block.set("rZ",f"{rotation}")
        block.set("sX",f"{xscale}")
        block.set("colR",f"{self.color_dict[color][0]}")
        block.set("colG",f"{self.color_dict[color][1]}")
        block.set("colB",f"{self.color_dict[color][2]}")
        
        self.block_count += 1
        return scene
        
    def Add_Blocks(self, scene):
        for block_data in self.block_list:
            pos = block_data[0]
            block = block_data[1]
            color = block_data[2]
            block_id = block[2]
            rotation = block[3]
            block_offset_x, block_offset_y = self.get_block_offset(block_id, rotation)
            
            # scene = self.Create_Block(scene, pos[0], pos[1],block[0],block[1],block[2],block[3],color)
            scene = self.Create_Block(scene, pos[1], pos[0], block_id, block_offset_x, block_offset_y, block[3], color)
        return scene
    
    def get_block_offset(self, blockID, rotation):
        block_data = BLOCK_SHAPES[blockID]
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
        return x_offset, y_offset

            
    def get_filename(self, filepath):
        filename = os.path.basename(filepath)
        dir_path = os.path.dirname(filepath)
        
        name, ext = os.path.splitext(filename)
        print(name, ext)
        
        optimized_filename = f"optimized_{name}{ext}"
        optimized_path = os.path.join(dir_path, optimized_filename)
        
        counter = 1
        while os.path.exists(optimized_path):
            optimized_filename = f"optimized{counter}_{name}{ext}"
            optimized_path = os.path.join(dir_path, optimized_filename)
            counter += 1

        return optimized_path

    def Write_To_File(self, root):
        xml_string = ET.tostring(root)
        filepath = self.get_filename(self.base_filepath)
        
        with lzma.open(filepath, "wb", format=lzma.FORMAT_ALONE) as output_file:
            output_file.write(xml_string)