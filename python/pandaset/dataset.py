from typing import overload, List, Dict

from .sequence import Sequence
from .utils import subdirectories


class DataSet:
    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._sequences: Dict[str, Sequence] = None
        self._load_sequences()

    @overload
    def __getitem__(self, item: int) -> Sequence:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[Sequence]:
        ...

    def __getitem__(self, item):
        return self._sequences[item]

    def _load_sequences(self) -> None:
        self._sequences = {}
        sequence_directories = subdirectories(self._directory)
        for sd in sequence_directories:
            seq_id = sd.split('/')[-1]
            self._sequences[seq_id] = Sequence(sd)

    def sequences(self) -> List[str]:
        return list(self._sequences.keys())


if __name__ == '__main__':
    pass
