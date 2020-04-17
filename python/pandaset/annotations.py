import glob
import json
import os
from abc import ABCMeta, abstractmethod
from typing import overload, List, TypeVar

import pandas as pd
from pandas.core.frame import DataFrame

T = TypeVar('T')


class Annotation:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def _data_file_extension(self) -> str:
        ...

    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._data_structure: List[str] = None
        self.data: List[DataFrame] = None
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

    def _load_data_structure(self) -> None:
        self._data_structure = sorted(
            glob.glob(f'{self._directory}/*.{self._data_file_extension}'))

    def load(self) -> None:
        self._load_data()

    def _load_data(self) -> None:
        self.data = []
        for fp in self._data_structure:
            self.data.append(self._load_data_file(fp))

    @abstractmethod
    def _load_data_file(self, fp: str) -> None:
        ...


class Cuboids(Annotation):
    @property
    def _data_file_extension(self) -> str:
        return 'pkl.gz'

    def __init__(self, directory: str) -> None:
        Annotation.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> pd.DataFrame:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[pd.DataFrame]:
        ...

    def __getitem__(self, item):
        return super().__getitem__(item)

    def _load_data_file(self, fp: str) -> None:
        return pd.read_pickle(fp)


class SemanticSegmentation(Annotation):
    @property
    def _data_file_extension(self) -> str:
        return 'pkl.gz'

    def __init__(self, directory: str) -> None:
        self._classes_structure: str = None
        self.classes: DataFrame = None
        Annotation.__init__(self, directory)

    @overload
    def __getitem__(self, item: int) -> pd.DataFrame:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[pd.DataFrame]:
        ...

    def __getitem__(self, item):
        return super().__getitem__(item)

    def load(self) -> None:
        super().load()
        self._load_classes()

    def _load_structure(self) -> None:
        super()._load_structure()
        self._load_classes_structure()

    def _load_classes_structure(self) -> None:
        classes_file = f'{self._directory}/classes.json'
        if os.path.isfile(classes_file):
            self._classes_structure = classes_file

    def _load_data_file(self, fp: str) -> None:
        return pd.read_pickle(fp)

    def _load_classes(self) -> None:
        with open(self._classes_structure, 'r') as f:
            file_data = json.load(f)
            self.classes = file_data


if __name__ == '__main__':
    pass
