#!/usr/bin/env python3
import json
import os.path
from abc import ABCMeta, abstractmethod
from typing import TypeVar, List, overload, Dict

T = TypeVar('T')


class Meta:
    """Meta class inherited by subclasses for more specific meta data types.

    ``Meta`` provides generic preparation and loading methods for PandaSet folder structures. Subclasses
    for specific meta data types must implement certain methods, as well as can override existing ones for extension.

    Args:
         directory: Absolute or relative path where annotation files are stored

    Attributes:
        data: List of meta data objects. The type of list elements depends on the subclass specific meta data type.
    """
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def _filename(self) -> str:
        ...

    @property
    def data(self) -> List[T]:
        """Returns meta data array.

        Subclasses can use any type inside array.
        """
        return self._data

    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._data_structure: str = None
        self._data: List[T] = None
        self._load_data_structure()

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[T]:
        ...

    def __getitem__(self, item):
        return self._data[item]

    def load(self) -> None:
        """Loads all meta data files from disk into memory.

        All meta data files are loaded into memory in filename order.
        """
        self._load_data()

    def _load_data_structure(self) -> None:
        meta_file = f'{self._directory}/{self._filename}'
        if os.path.isfile(meta_file):
            self._data_structure = meta_file

    def _load_data(self) -> None:
        self._data = []
        with open(self._data_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self._data.append(entry)


class GPS(Meta):
    """GPS data for each timestamp in this sequence.

    ``GPS`` provides GPS data for each timestamp. GPS data can be retrieved by slicing an instanced ``GPS`` class. (see example)

    Args:
         directory: Absolute or relative path where annotation files are stored

    Attributes:
        data: List of meta data objects. The type of list elements depends on the subclass specific meta data type.

    Examples:
        Assuming an instance `s` of class ``Sequence``, you can get GPS data for the first 5 frames in the sequence as follows:
        >>> s.load_gps()
        >>> gps_data_0_5 = s.gps[:5]
        >>> print(gps_data_0_5)
        [{'lat': 37.776089291519924, 'long': -122.39931707791749, 'height': 2.950900131607181, 'xvel': 0.0014639192106827986, 'yvel': 0.15895995994754034}, ...]
    """
    @property
    def _filename(self) -> str:
        return 'gps.json'

    @property
    def data(self) -> List[Dict[str, float]]:
        """Returns GPS data array.

        For every timestamp in the sequence, the GPS data contains vehicle latitude, longitude, height and velocity.

        Returns:
            List of dictionaries. Each dictionary has `str` keys and return types as follows:
                - `lat`: `float`
                    - Latitude in decimal degree format. Positive value corresponds to North, negative value to South.
                - `long`: `float`
                    - Longitude in decimal degree format. Positive value indicates East, negative value to West.
                - `height`: `float`
                    - Measured height in meters.
                - `xvel`: `float`
                    - Velocity in m/s
                - `yvel`: `float`
                    - Velocity in m/s

        """
        return self._data

    def __init__(self, directory: str) -> None:
        Meta.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> Dict[str, T]:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[Dict[str, T]]:
        ...

    def __getitem__(self, item):
        return self._data[item]


class Timestamps(Meta):
    @property
    def _filename(self) -> str:
        return 'timestamps.json'

    @property
    def data(self) -> List[float]:
        """Returns timestamp array.

        For every frame in this sequence, this property stores the recorded timestamp.

        Returns:
            List of timestamps as `float`
        """
        return self._data

    def __init__(self, directory: str) -> None:
        Meta.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> float:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[float]:
        ...

    def __getitem__(self, item):
        return self._data[item]


if __name__ == '__main__':
    pass
