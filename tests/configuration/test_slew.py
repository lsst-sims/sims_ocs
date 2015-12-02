import unittest

from lsst.sims.ocs.configuration.slew import Slew

class SlewTest(unittest.TestCase):

    def setUp(self):
        self.slew = Slew()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.slew.tel_optics_ol_slope, 1.0 / 3.5)
        self.assertEqual(len(self.slew.tel_optics_cl_delay), 2)
        self.assertEqual(self.slew.tel_optics_cl_delay[1], 20.0)
        self.assertEqual(len(self.slew.prereq_tel_optics_cl), 7)
        self.assertEqual(len(self.slew.prereq_readout), 0)
