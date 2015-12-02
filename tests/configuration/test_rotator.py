import unittest

from lsst.sims.ocs.configuration.rotator import Rotator

class RotatorTest(unittest.TestCase):

    def setUp(self):
        self.rotator = Rotator()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.rotator.minpos, -90.0)
        self.assertEqual(self.rotator.followsky, False)
