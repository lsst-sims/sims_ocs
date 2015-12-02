import unittest

from lsst.sims.ocs.configuration.camera import Camera

class CameraTest(unittest.TestCase):

    def setUp(self):
        self.camera = Camera()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.camera.filter_mounttime, 8 * 3600.0)
        self.assertEqual(len(self.camera.filter_mounted), 5)
        self.assertEqual(self.camera.filter_mounted[2], 'i')
