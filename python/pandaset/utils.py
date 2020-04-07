import os


def subdirectories(directory):
    return [d.path for d in os.scandir(directory) if d.is_dir()]
