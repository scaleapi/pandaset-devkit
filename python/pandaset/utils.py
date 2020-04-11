import os
from typing import List


def subdirectories(directory: str) -> List[str]:
    return [d.path for d in os.scandir(directory) if d.is_dir()]


if __name__ == '__main__':
    pass
