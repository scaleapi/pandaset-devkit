import glob
import pandas as pd


class Cuboids:
    def __init__(self, directory):
        self._directory = directory
        self._data_structure = None
        self.data = None
        self._load_data_structure()

    def _load_data_structure(self):
        self._data_structure = sorted(glob.glob(f'{self._directory}/*.pkl.gz'))

    def load_data(self, sl):
        self.data = []
        for fp in self._data_structure[sl]:
            self.data.append(
                pd.read_pickle(fp)
            )
