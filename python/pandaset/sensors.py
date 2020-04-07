import glob
import json
import os.path

import pandas as pd
from PIL import Image


class Sensor:
    def __init__(self, directory, data_file_extension):
        self._directory = directory
        self._data_file_extension = data_file_extension
        self._data_structure = None
        self.data = None
        self._poses_structure = None
        self.poses = None
        self._timestamps_structure = None
        self.timestamps = None
        self._load_data_structure()

    def __getitem__(self, item):
        return self.data[item]

    def _load_data_structure(self):
        self._data_structure = sorted(glob.glob(f'{self._directory}/*.{self._data_file_extension}'))

        poses_file = f'{self._directory}/poses.json'
        if os.path.isfile(poses_file):
            self._poses_structure = poses_file

        timestamps_file = f'{self._directory}/timestamps.json'
        if os.path.isfile(timestamps_file):
            self._timestamps_structure = timestamps_file

    def load(self):
        self._load_data()
        self._load_poses()
        self._load_timestamps()

    def _load_data(self):
        self.data = []
        for fp in self._data_structure:
            self.data.append(
                self._load_data_file(fp)
            )

    def _load_poses(self):
        self.poses = []
        with open(self._poses_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self.poses.append(
                    entry
                )

    def _load_timestamps(self):
        self.timestamps = []
        with open(self._timestamps_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self.timestamps.append(
                    entry
                )

    def _load_data_file(self, fp):
        return None


class Lidar(Sensor):

    def __init__(self, directory):
        self._intrinsics_structure = None
        self.intrinsics = None
        Sensor.__init__(self, directory, 'pkl.gz')

    def _load_data_file(self, fp):
        return pd.read_pickle(fp)


class Camera(Sensor):
    def __init__(self, directory):
        Sensor.__init__(self, directory, 'jpg')
        self._load_intrinsics()

    def load(self):
        super().load()
        self._load_intrinsics()

    def _load_data_file(self, fp):
        return Image.open(fp)

    def _load_data_structure(self):
        super()._load_data_structure()
        self._load_intrinsics()

    def _load_intrinsics_structure(self):
        intrinsics_file = f'{self._directory}/intrinsics.json'
        if os.path.isfile(intrinsics_file):
            self._intrinsics_structure = intrinsics_file

    def _load_intrinsics(self):
        self.intrinsics = []
        with open(self._intrinsics_structure, 'r') as f:
            file_data = json.load(f)
            self.intrinsics = Intrinsics(
                fx=file_data['fx'],
                fy=file_data['fy'],
                cx=file_data['cx'],
                cy=file_data['cy']
            )


class Intrinsics:
    def __init__(self, fx, fy, cx, cy):
        self.fx = fx,
        self.fy = fy,
        self.cx = cx,
        self.cy = cy
