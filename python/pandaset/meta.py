import json
import os.path


class Meta:
    def __init__(self, directory, filename):
        self._directory = directory
        self._data_structure = None
        self.data = None
        self._load_data_structure()

    def __getitem__(self, item):
        return self.data[item]

    def load(self):
        self._load_data()

    def _load_data_structure(self):
        meta_file = f'{self._directory}/{self.filename}'
        if os.path.isfile(meta_file):
            self._data_structure = meta_file

    def _load_data(self):
        self.data = []
        with open(self._data_structure, 'r') as f:
            file_data = json.load(f)
            for entry in file_data:
                self.data.append(
                    entry
                )


class GPS(Meta):
    def __init__(self, directory):
        Meta.__init__(self, directory, 'gps.json')


class Timestamps(Meta):
    def __init__(self, directory):
        Meta.__init__(self, directory, 'timestamps.json')
