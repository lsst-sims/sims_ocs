import unittest

from lsst.ts.schedulerConfig.instrument import Rotator

class RotatorTest(unittest.TestCase):

    def setUp(self):
        self.rotator = Rotator()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.rotator.minpos, -90.0)
        self.assertEqual(self.rotator.filter_change_pos, 0.0)
        self.assertEqual(self.rotator.follow_sky, False)
