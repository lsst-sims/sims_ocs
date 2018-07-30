import unittest

from lsst.ts.schedulerConfig.instrument import ObservatoryVariation

class ObservatoryVariationTest(unittest.TestCase):

    def setUp(self):
        self.obs_var = ObservatoryVariation()

    def test_basic_information_after_creation(self):
        self.assertFalse(self.obs_var.apply_variation)
        self.assertEqual(self.obs_var.telescope_change, 0.0)
        self.assertEqual(self.obs_var.dome_change, 0.0)
