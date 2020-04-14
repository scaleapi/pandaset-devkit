# pandaset-devkit

![Header Animation](../assets/animations/semseg-photo-labels.gif)


## Overview

Welcome to the repository of the [Pandaset](https://pandaset.org/ "Pandaset Official Website") Devkit.

## Dataset
### Download

To download the data set, please visit the official [Pandaset](https://pandaset.org/ "Pandaset Official Website") webpage and signed up through the form.
You will then be forwarded to a page with download links to the raw data and annotations.

### Unpack

Unpack the archive into any directory on your hard disk. The path will be referenced in usage of `pandaset-devkit` later, and does not have to be in the same directory as your scripts.

### Structure

#### Files & Folders

```text
.
├── LICENSE.txt
├── annotations
│   ├── cuboids
│   │   ├── 00.pkl.gz
│   │   ├── 01.pkl.gz
│   │   ├── ...
│   │   ├── 78.pkl.gz
│   │   └── 79.pkl.gz
| [  // Semantic Segmentation is available for some scenes
│   └── semseg
│       ├── 00.pkl.gz
│       ├── 01.pkl.gz
│       ├── ...
│       ├── 78.pkl.gz
│       ├── 79.pkl.gz
│       └── classes.json
| ]
├── camera
│   ├── back_camera
│   │   ├── 00.jpg
│   │   ├── 01.jpg
│   │   ├── ...
│   │   ├── 78.jpg
│   │   ├── 79.jpg
│   │   ├── intrinsics.json
│   │   ├── poses.json
│   │   └── timestamps.json
│   ├── front_camera
│   │   └── ...
│   ├── front_left_camera
│   │   └── ...
│   ├── front_right_camera
│   │   └── ...
│   ├── left_camera
│   │   └── ...
│   └── right_camera
│       └── ...
├── lidar
│   ├── 00.pkl.gz
│   ├── 01.pkl.gz
│   ├── ...
│   ├── 78.pkl.gz
│   ├── 79.pkl.gz
│   ├── poses.json
│   └── timestamps.json
└── meta
    ├── gps.json
    └── timestamps.json
```

## Instructions

### Setup

1. Create a Python>=3.6 environment with `pip` installed.
2. Clone the repository `git clone git@github.com:scaleapi/pandaset-devkit.git`
3. `cd` into `pandaset-devkit/python`
4. Execute `pip install .`

The `pandaset-devkit` is now installed in your Python>=3.6 environment and can be used.

### Usage

To get familiar with the API you can use the test sequence which is available in this repo under `test/data`, or you can point directly to the downloaded data set.

#### Initilization
First we need to create a `DataSet` object which searches for sequences.
```python
from pandaset import DataSet
dataset = DataSet('test/data')
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
The devkit will automatically search the sequence directory for available sensor data, meta data and annotations and prepare the directory to be loaded explicitly. At this point no point clouds or images have been loaded into memory.
To execute the loading of sensor and meta data into memory, we simply call the `load()` method on the sequence object. This will load all available sensor and meta data. 
```python
seq002.load()
```

If only certain data is required for analysis, there are more specific methods available which can also be chained to each other.
```python
seq002.load_lidar().load_cuboids()
```

#### Data Access

##### LiDAR
The LiDAR point clouds are stored as [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) and therefore allow to leverage their extensive API for data manipulation. This includes the simple return as a [numpy.ndarray](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html).
```python
pc0 = seq002.lidar[0]  # Returns the first LiDAR frame in sequence
print(pc0.columns)  # Index(['x', 'y', 'z', 'i', 't', 'd'], dtype='object')
```
```python
pc0_np = seq002.lidar[0].values  # Returns the first LiDAR frame in the sequence as an numpy ndarray
```

The LiDAR points are stored in a world coordinate system, therefore it is not required to transform them using the vehicle's pose graph. This allows to query all LiDAR frames in the sequence or a certain sampling rate and simply visualize them using your preferred library.
```python
pc_all = seq002.lidar[:]  # Returns all LiDAR frames from the sequence
```
```python
pc_sampled = seq002.lidar[::2]  # Returns every second LiDAR frame from the sequence
```

In addition to the LiDAR points, the `lidar` object also holds the sensor pose (`lidar.poses`) in world coordinate system and timestamp (`lidar.timestamps`) for every LiDAR frame recorded. Both objects can be sliced in the same way as the `lidar` object holding the point clouds.
```python
# Extract every fifth frame including sensor pose and timestamps
sl = slice(None, None, 5)  # Equivalent to [::5]

lidar_obj = seq002.lidar

pcs = lidar_obj[sl]
poses = lidar_obj.poses[sl]
timestamps = lidar_obj.timestamps[sl]
```


##### Cameras
Since the recording vehicle was equipped with multiple cameras, first we need to list which cameras have been used to record the sequence.
```python
print(seq002.camera.keys())  # ['front_camera', 'left_camera', 'back_camera', 'right_camera', 'front_left_camera', 'front_right_camera']
```
The camera count and names should be equal for all sequences.

Each camera name has its recordings loaded as [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) object, and can be accessed via normal list slicing. In the following example, we select the first image from the front camera and display it using the Pillow library in Python.
```python
front_camera = seq002.camera['front_camera']
img0 = front_camera[0]
img0.show()
```
Afterwards the extensive Pillow Image API can be used for image manipulation, conversion or export.

Similar to the `Lidar` object, each `Camera` object has properties which hold the camera pose (`camera.poses`) and timestamp (`camera.timestamps`) for every recorded frame, as well as the camera intrinsics (`camera.intrinsics`).
Again, the objects can be sliced the same way as the `Camera` object:

```python
# Extract every fifth frame including sensor pose and timestamps, plus intrinsics
sl = slice(None, None, 5)  # Equivalent to [::5]

camera_obj = seq002.camera['front_camera']

pcs = camera_obj[sl]
poses = camera_obj.poses[sl]
timestamps = camera_obj.timestamps[sl]
intrinsics = camera_obj.intrinsics 
```

#### Meta
In addition to the sensor data, the loaded data set also contains the following meta information:
* GPS Positions
* Timestamps

These can be directly accessed through the known list slicing operations, and read in their dict format. For example, the following example shows how to get the GPS coordinates of the vehicle on the first frame.
```python
pose0 = seq002.gps[0]
lat0 = pose0['lat']
long0 = pose0['long']
```

#### Annotations

##### Cuboids
The LiDAR Cuboid annotations are also stored inside the sequence object as a [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) for each timestamp.
The position coordinates (`position.x`,`position.y`,`position.z`) are located at the center of a cuboid. `dimensions.x` is the width of the cuboid from left to right, `dimensions.y` is the length of the cuboid from front to back and `dimensions.z` is the height of the cuboid from top to bottom.

```python
cuboids0 = seq002.cuboids[0]  # Returns the cuboid annotations for the first LiDAR frame in the sequence
print(cuboids0.columns)  # Index(['uuid', 'label', 'yaw', 'stationary', 'camera_used', 'position.x', 'position.y', 'position.z', 'dimensions.x', 'dimensions.y', 'dimensions.z', 'attributes.Object Motion', 'attributes.Rider Status', 'attributes.Pedestrian Behavior', 'attributes.Pedestrian Age'], dtype='object')
```

##### Semantic Segmentation
Analogous to the cuboid annotations, the Semantic Segmentation can be accessed using the `semseg` property on the sequence object. The index of each Semantic Segmentation data frame corresponds to the index of each LiDAR point cloud data frame, and can be joined using the index.
```python
semseg0 = seq002.semseg[0]  # Returns the semantic segmentation for the first LiDAR frame in the sequence
print(semseg0.columns)  # Index(['class'], dtype='object')
```


![Header Animation](../assets/static/montage-semseg-projection.jpg)