import unittest

from lsst.sims.ocs.configuration.slew import Slew
import SALPY_scheduler

class SlewTest(unittest.TestCase):

    def setUp(self):
        self.slew = Slew()
        self.slew_conf = SALPY_scheduler.scheduler_slewConfigC()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.slew.tel_optics_ol_slope, 1.0 / 3.5)
        self.assertEqual(len(self.slew.tel_optics_cl_delay), 2)
        self.assertEqual(self.slew.tel_optics_cl_delay[1], 20.0)
        self.assertEqual(len(self.slew.prereq_tel_optics_cl), 7)
        self.assertEqual(len(self.slew.prereq_readout), 0)

    def test_array_setting(self):
        self.slew.set_array(self.slew_conf, "tel_optics_cl_alt_limit")
        self.assertEqual(len(self.slew_conf.tel_optics_cl_alt_limit), 3)
        self.assertEqual(self.slew_conf.tel_optics_cl_alt_limit[2], 90.0)

    def test_string_setting(self):
        self.slew_conf.prereq_tel_settle = self.slew.get_string_rep("prereq_tel_settle")
        self.assertEqual(self.slew_conf.prereq_tel_settle, "TelAlt,TelAz")
