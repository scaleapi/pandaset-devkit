# pandaset-devkit

![Header Animation](../assets/animations/semseg-photo-labels.gif)


## Overview

Welcome to the repository of the [PandaSet](https://pandaset.org/ "Pandaset Official Website") Devkit.

## Dataset
### Download

To download the dataset, please visit the official [PandaSet](https://pandaset.org/ "Pandaset Official Website") webpage and sign up through the form.
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

To get familiar with the API you can point directly to the downloaded dataset.

#### Initialization
First, we need to create a `DataSet` object that searches for sequences.
```
>>> from pandaset import DataSet
>>> dataset = DataSet('/data/pandaset')
```
Afterwards we can list all the sequence IDs that have been found in the data folder.
```
>>> print(dataset.sequences())
['002',...]
```

Now, we access a specific sequence by choosing its key from the previously returned list, in this case sequence ID `'002'`
```
>>> seq002 = dataset['002']
```

API Reference: [DataSet class](https://scaleapi.github.io/pandaset-devkit/dataset.html#pandaset.dataset.DataSet)

#### Loading
The devkit will automatically search the sequence directory for available sensor data, metadata and annotations and prepare the directory to be loaded explicitly. At this point no point clouds or images have been loaded into memory.
To execute the loading of sensor data and metadata into memory, we simply call the `load()` method on the sequence object. This will load all available sensor data and metadata. 
```
>>> seq002.load()
```

If only certain data is required for analysis, there are more specific methods available, which can also be chained to each other.
```
>>> seq002.load_lidar().load_cuboids()
```

API Reference: [Sequence class](https://scaleapi.github.io/pandaset-devkit/sequence.html#pandaset.sequence.Sequence)

#### Data Access

##### LiDAR
The LiDAR point clouds are stored as [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) and therefore you are able to leverage their extensive API for data manipulation. This includes the simple return as a [numpy.ndarray](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html).
```
>>> pc0 = seq002.lidar[0]
>>> print(pc0)
                 x           y         z     i             t  d
index                                                          
0       -75.131138  -79.331690  3.511804   7.0  1.557540e+09  0
1      -112.588306 -118.666002  1.423499  31.0  1.557540e+09  0
2       -42.085902  -44.384891  0.593491   7.0  1.557540e+09  0
3       -27.329435  -28.795053 -0.403781   0.0  1.557540e+09  0
4        -6.196208   -6.621082  1.130009   3.0  1.557540e+09  0
            ...         ...       ...   ...           ... ..
166763   27.670526   17.159726  3.778677  25.0  1.557540e+09  1
166764   27.703935   17.114063  3.780626  27.0  1.557540e+09  1
166765   27.560664   16.955518  3.767948  18.0  1.557540e+09  1
166766   27.384433   16.783824  3.752670  22.0  1.557540e+09  1
166767   27.228821   16.626038  3.739154  20.0  1.557540e+09  1
[166768 rows x 6 columns]
```
```
>>> pc0_np = seq002.lidar[0].values  # Returns the first LiDAR frame in the sequence as an numpy ndarray
>>> print(pc0_np)
[[-7.51311379e+01 -7.93316897e+01  3.51180427e+00  7.00000000e+00
   1.55753996e+09  0.00000000e+00]
 [-1.12588306e+02 -1.18666002e+02  1.42349938e+00  3.10000000e+01
   1.55753996e+09  0.00000000e+00]
 [-4.20859017e+01 -4.43848908e+01  5.93490847e-01  7.00000000e+00
   1.55753996e+09  0.00000000e+00]
 ...
 [ 2.75606640e+01  1.69555183e+01  3.76794770e+00  1.80000000e+01
   1.55753996e+09  1.00000000e+00]
 [ 2.73844334e+01  1.67838237e+01  3.75266969e+00  2.20000000e+01
   1.55753996e+09  1.00000000e+00]
 [ 2.72288210e+01  1.66260378e+01  3.73915448e+00  2.00000000e+01
   1.55753996e+09  1.00000000e+00]]
```

The LiDAR points are stored in a world coordinate system; therefore it is not required to transform them using the vehicle's pose graph. This allows you to query all LiDAR frames in the sequence or a certain sampling rate and simply visualize them using your preferred library.
```
>>> pc_all = seq002.lidar[:]  # Returns all LiDAR frames from the sequence
```
```
>>> pc_sampled = seq002.lidar[::2]  # Returns every second LiDAR frame from the sequence
```

In addition to the LiDAR points, the `lidar` property also holds the sensor pose (`lidar.poses`) in world coordinate system and timestamp (`lidar.timestamps`) for every LiDAR frame recorded. Both objects can be sliced in the same way as the `lidar` property holding the point clouds.
```
>>> sl = slice(None, None, 5)  # Equivalent to [::5]  # Extract every fifth frame including sensor pose and timestamps
>>> lidar_obj = seq002.lidar
>>> pcs = lidar_obj[sl]
>>> poses = lidar_obj.poses[sl]
>>> timestamps = lidar_obj.timestamps[sl]
>>> print( len(pcs) == len(poses) == len(timestamps) )
True
```

API Reference: [Lidar class](https://scaleapi.github.io/pandaset-devkit/sensors.html#pandaset.sensors.Lidar)

##### Cameras
Since the recording vehicle was equipped with multiple cameras, first we need to list which cameras have been used to record the sequence.
```
>>> print(seq002.camera.keys())
['front_camera', 'left_camera', 'back_camera', 'right_camera', 'front_left_camera', 'front_right_camera']
```
The camera count and names should be equal for all sequences.

Each camera name has its recordings loaded as [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) object, and can be accessed via normal list slicing. In the following example, we select the first image from the front camera and display it using the Pillow library in Python.
```
>>> front_camera = seq002.camera['front_camera']
>>> img0 = front_camera[0]
>>> img0.show()
```
Afterwards the extensive Pillow Image API can be used for image manipulation, conversion or export.

Similar to the `Lidar` object, each `Camera` object has properties that hold the camera pose (`camera.poses`) and timestamp (`camera.timestamps`) for every recorded frame, as well as the camera intrinsics (`camera.intrinsics`).
Again, the objects can be sliced the same way as the `Camera` object:

```
>>> sl = slice(None, None, 5)  # Equivalent to [::5]
>>> camera_obj = seq002.camera['front_camera']
>>> pcs = camera_obj[sl]
>>> poses = camera_obj.poses[sl]
>>> timestamps = camera_obj.timestamps[sl]
>>> intrinsics = camera_obj.intrinsics 
```

API Reference: [Camera class](https://scaleapi.github.io/pandaset-devkit/sensors.html#pandaset.sensors.Camera)

#### Meta
In addition to the sensor data, the loaded dataset also contains the following meta information:
* GPS Positions
* Timestamps

These can be directly accessed through the known list slicing operations, and read in their dict format. The following example shows how to get the GPS coordinates of the vehicle on the first frame.
```
>>> pose0 = seq002.gps[0]
>>> print(pose0['lat'])
37.776089291519924
>>> print(pose0['long'])
-122.39931707791749
```

API Reference: [GPS class](https://scaleapi.github.io/pandaset-devkit/meta.html#pandaset.meta.GPS)

API Reference: [Timestamps class](https://scaleapi.github.io/pandaset-devkit/meta.html#pandaset.meta.Timestamps)

#### Annotations

##### Cuboids
The LiDAR Cuboid annotations are also stored inside the sequence object as a [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) for each timestamp.
The position coordinates (`position.x`,`position.y`,`position.z`) are located at the center of a cuboid. `dimensions.x` is the width of the cuboid from left to right, `dimensions.y` is the length of the cuboid from front to back and `dimensions.z` is the height of the cuboid from top to bottom.

```
>>> cuboids0 = seq002.cuboids[0]  # Returns the cuboid annotations for the first LiDAR frame in the sequence
>>> print(cuboids0.columns)
Index(['uuid', 'label', 'yaw', 'stationary', 'camera_used', 'position.x',
       'position.y', 'position.z', 'dimensions.x', 'dimensions.y',
       'dimensions.z', 'attributes.object_motion', 'cuboids.sibling_id',
       'cuboids.sensor_id', 'attributes.rider_status',
       'attributes.pedestrian_behavior', 'attributes.pedestrian_age'],
      dtype='object')
```

API Reference: [Cuboids class](https://scaleapi.github.io/pandaset-devkit/annotations.html#pandaset.annotations.Cuboids)

##### Semantic Segmentation
Analogous to the cuboid annotations, the Semantic Segmentation can be accessed using the `semseg` property on the sequence object. The index of each Semantic Segmentation data frame corresponds to the index of each LiDAR point cloud data frame, and can be joined using the index.
```
>>> semseg0 = seq002.semseg[0]  # Returns the semantic segmentation for the first LiDAR frame in the sequence
>>> print(semseg0.columns)  # Index(['class'], dtype='object')
Index(['class'], dtype='object')
```

API Reference: [SemanticSegmentation class](https://scaleapi.github.io/pandaset-devkit/annotations.html#pandaset.annotations.SemanticSegmentation)



![Header Animation](../assets/static/montage-semseg-projection.jpg)