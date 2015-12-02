import unittest

from lsst.sims.ocs.configuration.dome import Dome

class DomeTest(unittest.TestCase):

    def setUp(self):
        self.dome = Dome()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.dome.alt_maxspeed, 1.75)
        self.assertEqual(self.dome.settle_time, 1.0)
