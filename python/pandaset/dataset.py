from .utils import subdirectories
from .sequence import Sequence


class DataSet:

    def __init__(self, directory):
        self._directory = directory
        self._sequences = {}
        self._load_sequences()

    def __getitem__(self, item):
        return self._sequences[item]

    def _load_sequences(self):
        sequence_directories = subdirectories(self._directory)
        for sd in sequence_directories:
            seq_id = sd.split('/')[-1]
            self._sequences[seq_id] = Sequence(sd)

    def sequences(self):
        return list(self._sequences.keys())
