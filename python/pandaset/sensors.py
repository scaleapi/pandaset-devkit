import glob
import pandas as pd
from PIL import Image
import os.path
import json


class Lidar:
    def __init__(self, directory):
        self._directory = directory
        self._data_structure = None
        self.data = None
        self._pose_structure = None
        self.poses = None
        self._timestamps_structure = None
        self.timestamps = None
        self._load_data_structure()

    def _load_data_structure(self):
        self._data_structure = sorted(glob.glob(f'{self._directory}/*.pkl.gz'))

        positions_file = f'{self._directory}/positions.json'
        if os.path.isfile(positions_file):
            self._pose_structure = positions_file

        timestamps_file = f'{self._directory}/timestamps.json'
        if os.path.isfile(timestamps_file):
            self._timestamps_structure = timestamps_file

    def load_data(self, sl):
        self.data = []
        for fp in self._data_structure[sl]:
            self.data.append(
                pd.read_pickle(fp)
            )
        self.load_positions(sl)
        self.load_timestamps(sl)

    def load_positions(self, sl):
        self.poses = []
        with open(self._pose_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data[sl]:
                self.poses.append(
                    entry
                )

    def load_timestamps(self, sl):
        self.timestamps = []
        with open(self._timestamps_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data[sl]:
                self.timestamps.append(
                    entry
                )


class Camera:
    def __init__(self, directory):
        self._directory = directory
        self._data_structure = None
        self.data = None
        self._pose_structure = None
        self.poses = None
        self._timestamps_structure = None
        self.timestamps = None
        self._load_data_structure()

    def _load_data_structure(self):
        self._data_structure = sorted(glob.glob(f'{self._directory}/*.jpg'))

        positions_file = f'{self._directory}/positions.json'
        if os.path.isfile(positions_file):
            self._pose_structure = positions_file

        timestamps_file = f'{self._directory}/timestamps.json'
        if os.path.isfile(timestamps_file):
            self._timestamps_structure = timestamps_file

    def load_data(self, sl):
        self.data = []
        for fp in self._data_structure[sl]:
            self.data.append(
                Image.open(fp)
            )
        self.load_positions(sl)
        self.load_timestamps(sl)

    def load_positions(self, sl):
        self.poses = []
        with open(self._pose_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data[sl]:
                self.poses.append(
                    entry
                )

    def load_timestamps(self, sl):
        self.timestamps = []
        with open(self._timestamps_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data[sl]:
                self.timestamps.append(
                    entry
                )
