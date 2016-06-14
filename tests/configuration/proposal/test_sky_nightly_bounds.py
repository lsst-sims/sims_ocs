import unittest

from lsst.sims.ocs.configuration.proposal import SkyNightlyBounds

class SkyNightlyBoundsTest(unittest.TestCase):

    def setUp(self):
        self.sky_nightly_bounds = SkyNightlyBounds()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sky_nightly_bounds.twilight_boundary, -12.0)
        self.assertEqual(self.sky_nightly_bounds.delta_lst, 30.0)
