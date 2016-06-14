import unittest

from lsst.sims.ocs.configuration.instrument import OpticsLoopCorr
import SALPY_scheduler

class OpticsLoopCorrTest(unittest.TestCase):

    def setUp(self):
        self.olc = OpticsLoopCorr()
        self.olc_conf = SALPY_scheduler.scheduler_opticsLoopCorrConfigC()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.olc.tel_optics_ol_slope, 1.0 / 3.5)
        self.assertEqual(len(self.olc.tel_optics_cl_delay), 2)
        self.assertEqual(self.olc.tel_optics_cl_delay[1], 20.0)

    def test_array_setting(self):
        self.olc.set_array(self.olc_conf, "tel_optics_cl_alt_limit")
        self.assertEqual(len(self.olc_conf.tel_optics_cl_alt_limit), 3)
        self.assertEqual(self.olc_conf.tel_optics_cl_alt_limit[2], 90.0)
