#!/usr/bin/env python3
import glob
import json
import os
from abc import ABCMeta, abstractmethod
from typing import overload, List, TypeVar, Dict

import pandas as pd

T = TypeVar('T')


class Annotation:
    """Meta class inherited by subclasses for more specific annotation types.

    ``Annotation`` provides generic preparation and loading methods for PandaSet folder structures. Subclasses
    for specific annotation styles must implement certain methods, as well as can override existing ones for extension.

    Args:
         directory: Absolute or relative path where annotation files are stored

    Attributes:
        data: List of annotation data objects. The type of list elements depends on the subclass implementation of protected method ``_load_data_file``
    """
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def _data_file_extension(self) -> str:
        ...

    @property
    def data(self) -> List[T]:
        """Returns annotation data array.

        Subclasses can use any type inside array.
        """
        return self._data

    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._data_structure: List[str] = None
        self._data: List[T] = None
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
        """Loads all annotation files from disk into memory.

        All annotation files are loaded into memory in filename order.
        """
        self._load_data()

    def _load_data(self) -> None:
        self._data = []
        for fp in self._data_structure:
            self._data.append(self._load_data_file(fp))

    @abstractmethod
    def _load_data_file(self, fp: str) -> None:
        ...


class Cuboids(Annotation):
    """Loads and provides Cuboid annotations. Subclass of ``Annotation``.

    ``Cuboids`` loads files in `{sequence_id}/annotations/annotations/cuboids/` containing cuboid annotations.

    Args:
         directory: Absolute or relative path where annotation files are stored

    Attributes:
        data: List of cuboids for each frame of scene.
    """

    @property
    def _data_file_extension(self) -> str:
        return 'pkl.gz'

    @property
    def data(self) -> List[pd.DataFrame]:
        """Returns annotation data array.

        Returns:
            List of cuboid data frames. Each data frame has columns as follows:
                - index: `int`
                    - Each row corresponds to one cuboid. The index order is arbitrary.
                - `uuid`: `str
                    - Unique identifier for an object. If object is tracked within the sequence, the `uuid` stays the same on every frame.
                - `label`: `str`
                    - Contains name of object class associated with drawn cuboid.
                - `yaw`: `str`
                    - Rotation of cuboid around the z-axis. Given in _radians_ from which the cuboid is rotated along the z-axis. 0 radians is equivalent to the direction of the vector `(0, 1, 0)`. The vector points at the length-side. Rotation happens counter-clockwise, i.e., PI/2 is pointing in the same direction as the vector `(-1, 0, 0)`.
                - `stationary`: `bool`
                    - `True` if object is stationary in the whole scene, e.g., a parked car or traffic light. Otherwise `False`.
                - `camera_used`: `int`
                    - Reference to the camera which was used to validate cuboid position in projection. If no camera was explicitly used, value is set to `-1`.
                - `position.x`: `float`
                    - Position of the cuboid expressed as the center of the cuboid. Value is in world-coordinate system.
                - `position.y`: `float`
                    - Position of the cuboid expressed as the center of the cuboid. Value is in world-coordinate system.
                - `position.z`: `float`
                    - Position of the cuboid expressed as the center of the cuboid. Value is in world-coordinate system.
                - `dimensions.x`: `float`
                    - The dimensions of the cuboid based on the world dimensions. Width of the cuboid from left to right.
                - `dimensions.y`: `float`
                    - The dimensions of the cuboid based on the world dimensions. Length of the cuboid from front to back.
                - `dimensions.z`: `float`
                    - The dimensions of the cuboid based on the world dimensions. Height of the cuboid from top to bottom.
                - `attributes.object_motion`: `str`
                    - Values are `Parked`, `Stopped` or `Moving`.
                    - Set for cuboids with `label` values in
                        - _Car_
                        - _Pickup Truck_
                        - _Medium-sized Truck_
                        - _Semi-truck_
                        - _Towed Object_
                        - _Motorcycle_
                        - _Other Vehicle - Construction Vehicle_
                        - _Other Vehicle - Uncommon_
                        - _Other Vehicle - Pedicab_
                        - _Emergency Vehicle_
                        - _Bus_
                        - _Personal Mobility Device_
                        - _Motorized Scooter_
                        - _Bicycle_
                        - _Train_
                        - _Trolley_
                        - _Tram / Subway_
                - `attributes.rider_status`: `str`
                    - Values are `With Rider` or `Without Rider`.
                    - Set for cuboids with `label` values in
                        - _Motorcycle_
                        - _Personal Mobility Device_
                        - _Motorized Scooter_
                        - _Bicycle_
                        - _Animals - Other_
                - `attributes.pedestrian_behavior`: `str`
                    - Value are `Sitting`, `Lying`, `Walking` or `Standing`
                    - Set for cuboids with `label` values in
                        - _Pedestrian_
                        - _Pedestrian with Object_
                - `attributes.pedestrian_age`: `str`
                    - Value are `Adult` or `Child` (less than ~18 years old)
                    - Set for cuboids with `label` values in
                        - _Pedestrian_
                        - _Pedestrian with Object_
                - `cuboids.sensor_id`: `int`
                    - For the overlap area between mechanical 360° LiDAR and front-facing LiDAR, moving objects received two cuboids to compensate for synchronization differences of both sensors. If cuboid is in this overlapping area and moving, this value is either `0` (mechanical 360° LiDAR) or `1` (front-facing LiDAR). All other cuboids have value `-1`.
                - `cuboids.sibling_id`: `str`
                    - For cuboids which have `cuboids.sensor_id` set to `0` or `1`: this field stores the `uuid` of the sibling cuboid, i.e., measuring the same object in the overlap region, but with the other respective sensor.

        """
        return self._data

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
    """Loads and provides Semantic Segmentation annotations. Subclass of ``Annotation``.

    ``SemanticSegmentation`` loads files in `{sequence_id}/annotations/annotations/semseg/` containing semantic segmentation annotations for point clouds and class name mapping.

    Args:
         directory: Absolute or relative path where annotation files are stored

    Attributes:
        data: List of points and their class ID for each frame.
        classes: Dict containing class ID to class name mapping.
    """

    @property
    def _data_file_extension(self) -> str:
        return 'pkl.gz'

    @property
    def data(self) -> List[pd.DataFrame]:
        """Returns annotation data array.

        Returns:
            List of semantic segmentation data frames. Each data frame has columns as follows:
                - index: `int`
                    - Index order corresponds to the order of point cloud in ``lidar`` property.
                - `class`: `str`
                    - Class ID as a number in string format. Can be used to find class name from ``classes`` property.
        """
        return self._data

    @property
    def classes(self) -> Dict[str, str]:
        """Returns class id to class name mapping.

        Returns:
            Dictionary with class ID as key and class name as value. Valid for the complete scene.
        """
        return self._classes

    def __init__(self, directory: str) -> None:
        self._classes_structure: str = None
        self._classes: Dict[str, str] = None
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
            self._classes = file_data


if __name__ == '__main__':
    pass
