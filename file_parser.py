import lzma
import xml.etree.ElementTree as ET
import numpy as np

from block_data import BLOCK_SHAPES

MAX_LEVEL_SIZE = (110,88)

class FileParser():
    def __init__(self):
        self.tree = None
        self.root = None
    
    def parse_file(self, file_path):
        with lzma.open(file_path, 'rt', encoding='utf-8') as file:
            self.tree = ET.parse(file)
            self.root = self.tree.getroot()
            
    def create_block_array(self, root):
        pass
            
    