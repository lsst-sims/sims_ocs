import unittest

from lsst.ts.schedulerConfig.proposal import SkyConstraints

class SkyConstraintsTest(unittest.TestCase):

    def setUp(self):
        self.sky_constraints = SkyConstraints()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sky_constraints.max_airmass, 2.5)
        self.assertEqual(self.sky_constraints.max_cloud, 0.7)
        self.assertEqual(self.sky_constraints.min_distance_moon, 30.0)
        self.assertTrue(self.sky_constraints.exclude_planets)
