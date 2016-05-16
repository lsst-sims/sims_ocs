from __future__ import division
import unittest

from lsst.sims.ocs.configuration import Observatory
from lsst.sims.ocs.observatory import VariationalModel

class VariationalModelTest(unittest.TestCase):

    def setUp(self):
        self.var = VariationalModel(Observatory())
        self.tolerance = 1.0e-3

    def set_change_config(self):
        self.var.config.obs_var.apply_variation = True
        self.var.config.obs_var.telescope_change = 80.0
        self.var.config.obs_var.dome_change = 80.0

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.var.config)
        self.assertFalse(self.var.active)

    def test_modify_parameters(self):
        self.set_change_config()
        mod_dict = self.var.modify_parameters(2281, 3650)
        self.assertAlmostEqual(mod_dict["telescope"]["azimuth_maxspeed"], 3.5, delta=self.tolerance)
        self.assertAlmostEqual(mod_dict["dome"]["altitude_maxspeed"], 0.875, delta=self.tolerance)

    def test_change_speeds_and_accelerations(self):
        self.set_change_config()
        telescope = self.var.config.telescope.toDict()
        time_frac = 2281 / 3650
        self.var.change_speeds_and_accelerations(telescope,
                                                 self.var.config.obs_var.telescope_change,
                                                 time_frac)
        self.assertAlmostEqual(telescope["azimuth_maxspeed"], 3.5, delta=self.tolerance)
