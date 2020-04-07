from .utils import subdirectories
from .sensors import Lidar
from .sensors import Camera
from .meta import GPS
from .meta import Timestamps
from .annotations import Cuboids


class Sequence:
    def __init__(self, directory):
        self._directory = directory
        self.lidar = None
        self.camera = None
        self.gps = None
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
                    camera_name = cd.split('/')[-1]
                    self.camera[camera_name] = Camera(cd)
            if dd.endswith('meta'):
                self.gps = GPS(dd)
                self.timestamps = Timestamps(dd)
            if dd.endswith('annotations'):
                annotation_directories = subdirectories(dd)
                for ad in annotation_directories:
                    if ad.endswith('cuboids'):
                        self.cuboids = Cuboids(ad)

    def load(self):
        self.load_lidar()
        self.load_camera()
        self.load_gps()
        self.load_timestamps()
        self.load_cuboids()

    def load_lidar(self):
        self.lidar.load()
        return self

    def load_camera(self):
        for cam in self.camera.values():
            cam.load()
        return self

    def load_gps(self):
        self.gps.load()
        return self

    def load_timestamps(self):
        self.timestamps.load()
        return self

    def load_cuboids(self):
        self.cuboids.load()
        return self
