from file_parser import FileParser
from auto_optimizer import AutoOptimizer
from file_writer import SnapshotCreator

class LevelHander():
    def __init__(self):
        self.fp = FileParser()
        self.filepath = None
        
    def set_filepath(self, filepath):
        self.filepath = filepath
        
    def optimize_level(self):
        map_data = self.fp.parse_file(self.filepath)
        ao = AutoOptimizer(map_data['grid'], map_data['color_dict'])
        map_file = SnapshotCreator(ao, map_data, self.filepath)