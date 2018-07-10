import unittest

from lsst.ts.schedulerConfig.environment import Environment

class EnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.environ = Environment()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.environ.seeing_db, "")
        self.assertEqual(self.environ.cloud_db, "")
        self.assertEqual(self.environ.telescope_seeing, 0.25)
        self.assertEqual(self.environ.optical_design_seeing, 0.08)
        self.assertEqual(self.environ.camera_seeing, 0.3)
        self.assertEqual(self.environ.scale_to_eff, 1.16)
        self.assertEqual(self.environ.geom_eff_factor, 1.04)
