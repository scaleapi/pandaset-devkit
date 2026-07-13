"""Tests for LiDAR file extension fallback (#140)."""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from pandaset.sensors import Lidar


class TestLidarExtensions(unittest.TestCase):
    def test_loads_plain_pkl_when_gz_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pd.DataFrame({"x": [1.0], "y": [2.0]}).to_pickle(root / "00.pkl")
            (root / "poses.json").write_text("[]")
            (root / "timestamps.json").write_text("[]")
            lidar = Lidar(str(root))
            lidar.load()
            self.assertEqual(len(lidar.data), 1)
            self.assertIn("x", lidar.data[0].columns)


if __name__ == "__main__":
    unittest.main()
