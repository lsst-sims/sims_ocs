import unittest

from lsst.sims.ocs.configuration.instrument import Park

class ParkTest(unittest.TestCase):

    def setUp(self):
        self.park = Park()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.park.telescope_altitude, 86.5)
        self.assertEqual(self.park.telescope_azimuth, 0.0)
        self.assertEqual(self.park.telescope_rotator, 0.0)
        self.assertEqual(self.park.dome_altitude, 90.0)
        self.assertEqual(self.park.dome_azimuth, 0.0)
        self.assertEqual(self.park.filter_position, 'z')
