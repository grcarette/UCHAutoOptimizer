from file_parser import FileParser
from auto_optimizer import AutoOptimizer
from optimizer import BlockOptimizer
from file_writer import SnapshotCreator

class LevelHander():
    def __init__(self):
        self.fp = FileParser()
        self.filepath = None
        
    def set_filepath(self, filepath):
        self.filepath = filepath
        
    def optimize_level(self):
        map_data = self.fp.parse_file(self.filepath)
        bo = BlockOptimizer()
        block_list = bo.optimize_level(map_data)
        map_file = SnapshotCreator(block_list, map_data, self.filepath)