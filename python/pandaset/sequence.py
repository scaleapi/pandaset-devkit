import os

from .utils import subdirectories
from .sensors import Lidar
from .sensors import Camera
from .meta import GPSPoses
from .meta import Timestamps
from .annotations import Cuboids


class Sequence:
    def __init__(self, directory):
        self._directory = directory
        self.lidar = None
        self.camera = None
        self.gps_poses = None
        self.timestamps = None
        self.cuboids = None
        self._load_data_structure()

    def _load_data_structure(self):
        data_directories = subdirectories(self._directory)

        for dd in data_directories:
            if dd.endswith('lidar'):
                self.lidar = Lidar(dd)
            if dd.endswith('camera'):
                self.camera = {}
                camera_directories = subdirectories(dd)
                for cd in camera_directories:
                    camera_name = os.path.split(cd)[-1]
                    self.camera[camera_name] = Camera(cd)
            if dd.endswith('meta'):
                self.gps_poses = GPSPoses(dd)
                self.timestamps = Timestamps(dd)
            if dd.endswith('annotations'):
                annotation_directories = subdirectories(dd)
                for ad in annotation_directories:
                    if ad.endswith('cuboids'):
                        self.cuboids = Cuboids(ad)

    def load(self, sl=(None, None, None)):
        self.load_lidar(sl)
        self.load_camera(sl)
        self.load_gps_poses(sl)
        self.load_timestamps(sl)
        self.load_cuboids(sl)

    def load_lidar(self, sl=(None, None, None)):
        self.lidar.load_data(slice(*sl))

    def load_camera(self, sl=(None, None, None)):
        for c in self.camera.values():
            c.load_data(slice(*sl))

    def load_gps_poses(self, sl=(None, None, None)):
        self.gps_poses.load_data(slice(*sl))

    def load_timestamps(self, sl=(None, None, None)):
        self.timestamps.load_data(slice(*sl))

    def load_cuboids(self, sl=(None, None, None)):
        self.cuboids.load_data(slice(*sl))
