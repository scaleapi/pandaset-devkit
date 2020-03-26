# pandaset-devkit

![Header Animation](../assets/animations/semseg-photo-labels.gif)


## Overview

Welcome to the repository of the [Pandaset](https://pandaset.org/ "Pandaset Official Website") Devkit.

## Dataset
### Download

To download the data set, please visit the official [Pandaset](https://pandaset.org/ "Pandaset Official Website") webpage and signed up through the form.
You will then be forwarded to a page with download links to the raw data and annotations.

### Unpack

Unpack the archive into any directory on your hard disk. The path will be referenced by the `pandaset-devkit` later, and does not have to be in the same directory.

## Instructions

### Setup

1. Create a Python>=3.6 environment with `pip` installed.
2. Clone the repository `git clone git@github.com:scaleapi/pandaset-devkit.git`
3. `cd` into `./pandaset-devkit/python`
4. Execute `pip install .`

The `pandaset-devkit` is now installed in your Python>=3.6 environment and can be used.

### Usage

To get familiar with the API we can use the test sequence which is available in this repo under `./test/data`, or we can point directly to the downloaded data set.

#### Initilization
First we need to create a `DataSet` object which searches for sequences.
```python
from pandaset import DataSet
dataset = DataSet('./test/data')
```
Afterwards we can list all the sequence IDs which have been found in the data folder.
```python
print(dataset.sequences())  # ['002']
```

Now we access a specific sequence by choosing its key from the previously returned list, in this case sequence ID `'002'`
```python
seq002 = dataset['002']
```

#### Loading
The devkit will automatically search the sequence directory for available sensor and meta data and prepare the path for a loading step. At this point no point clouds or images have been loaded into memory.
To execute the loading of sensor and meta data into memory, we simply call the `load()` method on the sequence object. This will load all available sensor and meta data. If only specific sensors or meta data is required, there are more specific methods available.
```python
seq002.load()

# OR

seq002.load_lidar()
seq002.load_camera()
seq002.load_gps_poses()
seq002.load_timestamps()
seq002.load_cuboids()
```

Since not everybody might want to work with full sampling rate, each of the `load()` methods accept a _3-tuple_ which serves as a slicing information. In the following example, we want every second frame between frame 10 and frame 50 loaded. It is equivalent to slicing a python array using `my_array[10:50:2]`.
```python
seq002.load((10, 50, 2))
```

#### Data Access

##### LiDAR
The LiDAR point clouds are stored as [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) and therefore allow to leverage their extensive API for data manipulation. This includes the simple return as a [numpy.ndarray](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html).
```python
pc0 = seq002.lidar.data[0]
print(pc0.columns)  # Index(['x', 'y', 'z', 'i', 't', 'd'], dtype='object')

pc0_np = seq002.lidar.data[0].to_numpy()
# OR
pc0_np = seq002.lidar.data[0].values
```

##### Cameras
Since the recording vehicle was equipped with multiple cameras, first we need to list which cameras have been used to record the sequence.
```python
print(seq002.camera.keys())  # ['front_camera', 'left_camera', 'back_camera', 'right_camera', 'front_left_camera', 'front_right_camera']
```
Each camera name has its recordings loaded as [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) object, and can be accessed via normal list slicing. In the following example, we select the first image from the front camera and display it using the Pillow library in Python.
```python
front_camera = seq002.camera['front_camera']
img0 = front_camera.data[0]
img0.show()
```
Afterwards the extensive Pillow Image API can be used for image manipulation, conversion or export.

#### Meta
In addition to the sensor data, the loaded data set also contains the following meta information:
* Vehicle Poses
* Timestamps

These can be directly accessed through the known list slicing operations, and read in their dict format. For example, the following example shows how to get the GPS coordinates of the vehicle on the first frame.
```python
pose0 = seq002.gps_poses.data[0]
lat0 = pose0['lat']
long0 = pose0['long']
```

#### Annotations

The LiDAR Cuboid annotations are also stored inside the sequence object as a [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) for each timestamp.
The position coordinates (`positin.x`,`position.y`,`position.z`) are located at the center of a cuboid. `dimensions.x` is the width of the cuboid from left to right, `dimensions.y` is the length of the cuboid from front to back and `dimensions.z` is the height of the cuboid from top to bottom.

```python
cuboids0 = seq002.cuboids.data[0]
print(cuboids0.columns)  # Index(['uuid', 'label', 'yaw', 'stationary', 'camera_used', 'position.x', 'position.y', 'position.z', 'dimensions.x', 'dimensions.y', 'dimensions.z', 'attributes.Object Motion', 'attributes.Rider Status', 'attributes.Pedestrian Behavior', 'attributes.Pedestrian Age'], dtype='object')
```


![Header Animation](../assets/static/montage-semseg-projection.jpg)