#!/usr/bin/env python3
from typing import overload, List, Dict

from .sequence import Sequence
from .utils import subdirectories


class DataSet:
    """Top-level class to load PandaSet

        ``DataSet`` prepares and loads ``Sequence`` objects for every sequence found in provided directory.
        Access to a specific sequence is provided by using the sequence name as a key on the ``DataSet`` object.

        Args:
             directory: Absolute or relative path where PandaSet has been extracted to.

        Examples:
            >>> pandaset = DataSet('/data/pandaset')
            >>> s = pandaset['002']
        """

    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._sequences: Dict[str, Sequence] = None
        self._load_sequences()

    def __getitem__(self, item) -> Sequence:
        return self._sequences[item]

    def _load_sequences(self) -> None:
        self._sequences = {}
        sequence_directories = subdirectories(self._directory)
        for sd in sequence_directories:
            seq_id = sd.split('/')[-1].split('\\')[-1]
            self._sequences[seq_id] = Sequence(sd)

    def sequences(self, with_semseg: bool = False) -> List[str]:
        """ Lists all available sequence names

        Args:
            with_semseg: Set `True` if only sequences with semantic segmentation annotations should be returned. Set `False` to return all sequences (with or without semantic segmentation).

        Returns:
            List of sequence names.

        Examples:
            >>> pandaset = DataSet('/data/pandaset')
            >>> print(pandaset.sequences())
            ['002','004','080']


        """
        if with_semseg:
            return [s for s in list(self._sequences.keys()) if self._sequences[s].semseg]
        else:
            return list(self._sequences.keys())

    def unload(self, sequence: str):
        """ Removes all sequence file data from memory if previously loaded from disk.

        This is useful if you intend to iterate over all sequences and perform some
        operation. If you do not unload the sequences, it quickly leads to sigkill.

        Args:
            sequence: The sequence name

        Returns:
            None

        Examples:
            >>> pandaset = DataSet('...')
            >>> for sequence in pandaset.sequences():
            >>>     seq = pandaset[sequence]
            >>>     seq.load()
            >>>     # do operations on sequence here...
            >>>     # when finished, unload the sequence from memory
            >>>     pandaset.unload(sequence)

        """
        if sequence in self._sequences:
            del self._sequences[sequence]


if __name__ == '__main__':
    pass
