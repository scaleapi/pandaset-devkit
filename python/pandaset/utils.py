import os


def subdirectories(directory):
    return [d.path for d in os.scandir(directory) if d.is_dir()]

'''
def relative_paths(full_paths, base_path):
    return [os.path.relpath(fp, base_path) for fp in full_paths]
'''