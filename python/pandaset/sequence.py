import glob
from .utils import subdirectories
from .sensors import Lidar
from .sensors import Camera
import pandas as pd


class Sequence:

    def __init__(self, directory):
        self.directory = directory
        self.lidar = None
        self.camera = None
        self.load_data_structure()

    def load_data_structure(self):
        data_directories = subdirectories(self.directory)

        for dd in data_directories:
            if dd.endswith('lidar'):
                self.lidar = Lidar(dd)
            if dd.endswith('camera'):
                self.camera = {}
                camera_directories = subdirectories(dd)
                for cd in camera_directories:
                    camera_name = seq_id = cd.split('/')[-1]
                    self.camera[camera_name] = Camera(cd)

    def load_data(self, sl=(None, None, None)):
        data_slice = slice(*sl)
        self.lidar.load_data(data_slice)
        for c in self.camera.values():
            c.load_data(data_slice)
