from .utils import subdirectories
from .sequence import Sequence


class DataSet:

    def __init__(self, directory):
        self.directory = directory
        self.sequences = {}
        self.load_sequences()

    def __getitem__(self, item):
        return self.sequences[item]

    def load_sequences(self):
        sequence_directories = subdirectories(self.directory)
        for sd in sequence_directories:
            seq_id = sd.split('/')[-1]
            self.sequences[seq_id] = Sequence(sd)

    def sequences(self):
        return list(self.sequences.keys())
