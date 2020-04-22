from typing import Dict

from .annotations import Cuboids
from .annotations import SemanticSegmentation
from .meta import GPS
from .meta import Timestamps
from .sensors import Camera
from .sensors import Lidar
from .utils import subdirectories


class Sequence:
    def __init__(self, directory: str):
        self._directory: str = directory
        self.lidar: Lidar = None
        self.camera: Dict[str, Camera] = None
        self.gps: GPS = None
        self.timestamps: Timestamps = None
        self.cuboids: Cuboids = None
        self._load_data_structure()

    def _load_data_structure(self) -> None:
        data_directories = subdirectories(self._directory)

        for dd in data_directories:
            if dd.endswith('lidar'):
                self.lidar = Lidar(dd)
            elif dd.endswith('camera'):
                self.camera = {}
                camera_directories = subdirectories(dd)
                for cd in camera_directories:
                    camera_name = cd.split('/')[-1].split('\\')[-1]
                    self.camera[camera_name] = Camera(cd)
            elif dd.endswith('meta'):
                self.gps = GPS(dd)
                self.timestamps = Timestamps(dd)
            elif dd.endswith('annotations'):
                annotation_directories = subdirectories(dd)
                for ad in annotation_directories:
                    if ad.endswith('cuboids'):
                        self.cuboids = Cuboids(ad)
                    elif ad.endswith('semseg'):
                        self.semseg = SemanticSegmentation(ad)

    def load(self) -> 'Sequence':
        self.load_lidar()
        self.load_camera()
        self.load_gps()
        self.load_timestamps()
        self.load_cuboids()
        self.load_semseg()
        return self

    def load_lidar(self) -> 'Sequence':
        self.lidar.load()
        return self

    def load_camera(self) -> 'Sequence':
        for cam in self.camera.values():
            cam.load()
        return self

    def load_gps(self) -> 'Sequence':
        self.gps.load()
        return self

    def load_timestamps(self) -> 'Sequence':
        self.timestamps.load()
        return self

    def load_cuboids(self) -> 'Sequence':
        self.cuboids.load()
        return self

    def load_semseg(self) -> 'Sequence':
        if self.semseg:
            self.semseg.load()
        return self


if __name__ == '__main__':
    pass
