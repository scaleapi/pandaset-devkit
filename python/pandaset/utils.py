#!/usr/bin/env python3
import os
from typing import List


def subdirectories(directory: str) -> List[str]:
    """List all subdirectories of a directory.

    Args:
        directory: Relative or absolute path

    Returns:
        List of path strings for every subdirectory in `directory`.
    """
    return [d.path for d in os.scandir(directory) if d.is_dir()]


if __name__ == '__main__':
    pass
