import unittest

from lsst.sims.ocs.configuration.telescope import Telescope

class TelescopeTest(unittest.TestCase):

    def setUp(self):
        self.telescope = Telescope()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.telescope.azimuth_maxpos, 270.0)
        self.assertEqual(self.telescope.azimuth_maxspeed, 7.0)
        self.assertEqual(self.telescope.settle_time, 3.0)
