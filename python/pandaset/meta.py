import json
import os.path
from abc import ABCMeta, abstractmethod
from typing import TypeVar, List, overload, Dict

T = TypeVar('T')


class Meta:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def _filename(self) -> str:
        ...

    def __init__(self, directory: str):
        self._directory: str = directory
        self._data_structure: str = None
        self.data: List[T] = None
        self._load_data_structure()

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[T]:
        ...

    def __getitem__(self, item):
        return self.data[item]

    def load(self) -> None:
        self._load_data()

    def _load_data_structure(self) -> None:
        meta_file = f'{self._directory}/{self._filename}'
        if os.path.isfile(meta_file):
            self._data_structure = meta_file

    def _load_data(self) -> None:
        self.data = []
        with open(self._data_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self.data.append(entry)


class GPS(Meta):
    @property
    def _filename(self) -> str:
        return 'gps.json'

    def __init__(self, directory: str):
        Meta.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> Dict[str, T]:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[Dict[str, T]]:
        ...

    def __getitem__(self, item):
        return self.data[item]


class Timestamps(Meta):
    @property
    def _filename(self) -> str:
        return 'timestamps.json'

    def __init__(self, directory: str):
        Meta.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> float:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[float]:
        ...

    def __getitem__(self, item):
        return self.data[item]


if __name__ == '__main__':
    pass
