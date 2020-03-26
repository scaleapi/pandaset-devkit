import os.path
import json


class GPSPoses:
    def __init__(self, directory):
        self._directory = directory
        self._data_structure = None
        self.data = None
        self._load_data_structure()

    def _load_data_structure(self):
        meta_file = f'{self._directory}/gps_poses.json'
        if os.path.isfile(meta_file):
            self._data_structure = meta_file

    def load_data(self, sl):
        self.data = []
        with open(self._data_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data[sl]:
                self.data.append(
                    entry
                )


class Timestamps:
    def __init__(self, directory):
        self._directory = directory
        self._data_structure = None
        self.data = None
        self._load_data_structure()

    def _load_data_structure(self):
        meta_file = f'{self._directory}/timestamps.json'
        if os.path.isfile(meta_file):
            self._data_structure = meta_file

    def load_data(self, sl):
        self.data = []
        with open(self._data_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data[sl]:
                self.data.append(
                    entry
                )
