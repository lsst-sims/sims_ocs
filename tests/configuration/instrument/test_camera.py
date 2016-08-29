import unittest

from lsst.sims.ocs.configuration.instrument import Camera

class CameraTest(unittest.TestCase):

    def setUp(self):
        self.camera = Camera()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.camera.filter_mount_time, 8 * 3600.0)
        self.assertEqual(len(self.camera.filter_mounted), 5)
        self.assertEqual(self.camera.filter_mounted[2], 'i')
        self.assertEqual(self.camera.filter_max_changes_burst_num, 1)
        self.assertEqual(self.camera.filter_max_changes_burst_time, 0.0)
        self.assertEqual(self.camera.filter_max_changes_avg_num, 3000)
        self.assertEqual(self.camera.filter_max_changes_avg_time, 31557600.0)

    def test_properties(self):
        self.assertEqual(self.camera.filter_mounted_str, "g,r,i,z,y")
        self.assertEqual(self.camera.filter_removable_str, "y,z")
        self.assertEqual(self.camera.filter_unmounted_str, "u")
