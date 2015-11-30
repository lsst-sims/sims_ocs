import unittest

from lsst.sims.ocs.configuration.observatory import Observatory

class ObservatoryTest(unittest.TestCase):

    def setUp(self):
        self.observatory = Observatory()

    def test_basic_information_from_creation(self):
        # Pick random sampling of things for now.
        self.assertEqual(self.observatory.tel_az_maxpos, 270.0)
        self.assertEqual(self.observatory.tel_az_maxspeed, 7.0)
        self.assertEqual(self.observatory.rotator_minpos, -90.0)
        self.assertEqual(self.observatory.rotator_followsky, False)
        self.assertEqual(self.observatory.filter_mounttime, 8 * 3600.0)
        self.assertEqual(self.observatory.tel_optics_ol_slope, 1.0 / 3.5)
        self.assertEqual(len(self.observatory.tel_optics_cl_delay), 2)
        self.assertEqual(self.observatory.tel_optics_cl_delay[1], 20.0)
        self.assertEqual(len(self.observatory.filter_mounted), 5)
        self.assertEqual(self.observatory.filter_mounted[2], 'i')
        self.assertEqual(len(self.observatory.prereq_tel_optics_cl), 7)
        self.assertEqual(len(self.observatory.prereq_readout), 0)
