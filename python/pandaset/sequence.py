import glob
from .utils import subdirectories
import pandas as pd


class Sequence:

    def __init__(self, directory):
        self.directory = directory
        self.data_structure = {
            'lidar': {},
            'camera': {},
            'meta': {},
            'annotations': {}
        }
        self.data = {
            'lidar': [],
            'camera': {}
        }
        self.load_data_structure()

    def load_data_structure(self):
        data_directories = subdirectories(self.directory)

        for dd in data_directories:
            if dd.endswith('lidar'):
                self.load_lidar_data_structure(dd)

    def load_lidar_data_structure(self, directory):
        self.data_structure['lidar']['pointclouds'] = sorted(glob.glob(f'{directory}/*.pkl.gz'))

    def load_data(self):
        self.load_lidar_data()

    def load_lidar_data(self):
        self.data['lidar'] = []
        for lf in self.data_structure['lidar']['pointclouds']:
            self.data['lidar'].append(
                pd.read_pickle(lf)
            )
