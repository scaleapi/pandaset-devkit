import glob
import json
import os.path
from typing import List, overload, TypeVar, Dict
from abc import ABCMeta, abstractmethod

import pandas as pd
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from pandas.core.frame import DataFrame

T = TypeVar('T')


class Sensor:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def _data_file_extension(self) -> str:
        ...

    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._data_structure: List[str] = None
        self.data: List[T] = None
        self._poses_structure: str = None
        self.poses: List[Dict[str, T]] = None
        self._timestamps_structure: str = None
        self.timestamps: List[float] = None
        self._load_structure()

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[T]:
        ...

    def __getitem__(self, item):
        return self.data[item]

    def _load_structure(self) -> None:
        self._load_data_structure()
        self._load_poses_structure()
        self._load_timestamps_structure()

    def _load_data_structure(self) -> None:
        self._data_structure = sorted(
            glob.glob(f'{self._directory}/*.{self._data_file_extension}'))

    def _load_poses_structure(self) -> None:
        poses_file = f'{self._directory}/poses.json'
        if os.path.isfile(poses_file):
            self._poses_structure = poses_file

    def _load_timestamps_structure(self) -> None:
        timestamps_file = f'{self._directory}/timestamps.json'
        if os.path.isfile(timestamps_file):
            self._timestamps_structure = timestamps_file

    def load(self) -> None:
        self._load_data()
        self._load_poses()
        self._load_timestamps()

    def _load_data(self) -> None:
        self.data = []
        for fp in self._data_structure:
            self.data.append(self._load_data_file(fp))

    def _load_poses(self) -> None:
        self.poses = []
        with open(self._poses_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self.poses.append(entry)

    def _load_timestamps(self) -> None:
        self.timestamps = []
        with open(self._timestamps_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self.timestamps.append(entry)

    @abstractmethod
    def _load_data_file(self, fp: str) -> None:
        ...


class Lidar(Sensor):
    @property
    def _data_file_extension(self) -> str:
        return 'pkl.gz'

    def __init__(self, directory: str) -> None:
        Sensor.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> DataFrame:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[DataFrame]:
        ...

    def __getitem__(self, item):
        return super().__getitem__(item)

    def _load_data_file(self, fp: str) -> DataFrame:
        return pd.read_pickle(fp)


class Camera(Sensor):
    @property
    def _data_file_extension(self) -> str:
        return 'jpg'

    def __init__(self, directory: str) -> None:
        self._intrinsics_structure: str = None
        self.intrinsics: 'Camera._Intrinsics' = None
        Sensor.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> JpegImageFile:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[JpegImageFile]:
        ...

    def __getitem__(self, item):
        return super().__getitem__(item)

    def load(self) -> None:
        super().load()
        self._load_intrinsics()

    def _load_structure(self) -> None:
        super()._load_structure()
        self._load_intrinsics_structure()

    def _load_intrinsics_structure(self) -> None:
        intrinsics_file = f'{self._directory}/intrinsics.json'
        if os.path.isfile(intrinsics_file):
            self._intrinsics_structure = intrinsics_file

    def _load_data_file(self, fp: str) -> JpegImageFile:
        return Image.open(fp)

    def _load_intrinsics(self) -> None:
        with open(self._intrinsics_structure, 'r') as f:
            file_data = json.load(f)
            self.intrinsics = self._Intrinsics(fx=file_data['fx'],
                                               fy=file_data['fy'],
                                               cx=file_data['cx'],
                                               cy=file_data['cy'])

    class _Intrinsics:
        def __init__(self, fx: float, fy: float, cx: float, cy: float):
            self.fx: float = fx
            self.fy: float = fy
            self.cx: float = cx
            self.cy: float = cy


if __name__ == '__main__':
    pass
