import glob
import pandas as pd
from PIL import Image


class Lidar:

    def __init__(self, directory):
        self.directory = directory
        self.data_structure = []
        self.data = []
        self.load_data_structure()

    def load_data_structure(self):
        self.data_structure = sorted(glob.glob(f'{self.directory}/*.pkl.gz'))

    def load_data(self, sl):
        self.data = []
        for fp in self.data_structure[sl]:
            self.data.append(
                pd.read_pickle(fp)
            )


class Camera:

    def __init__(self, directory):
        self.directory = directory
        self.data_structure = []
        self.data = []
        self.load_data_structure()

    def load_data_structure(self):
        self.data_structure = sorted(glob.glob(f'{self.directory}/*.jpg'))

    def load_data(self, sl):
        for fp in self.data_structure[sl]:
            self.data.append(
                Image.open(fp)
            )
