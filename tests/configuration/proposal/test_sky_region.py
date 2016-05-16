import unittest

from lsst.sims.ocs.configuration.proposal import Selection, SkyRegion

class SkyRegionTest(unittest.TestCase):

    def setUp(self):
        self.sky_region = SkyRegion()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sky_region.twilight_boundary, -12.0)
        self.assertEqual(self.sky_region.delta_lst, 30.0)
        self.assertEqual(self.sky_region.dec_window, 90.0)
        self.assertIsNone(self.sky_region.limit_selections)
        self.assertFalse(self.sky_region.use_galactic_exclusion)
        self.assertIsNotNone(self.sky_region.galactic_exclusion)

    def test_limit_selections_assignment(self):
        self.sky_region.limit_selections = {"RA": Selection()}
        self.assertIsNotNone(self.sky_region.limit_selections)
        self.assertEqual(len(self.sky_region.limit_selections), 1)

    def test_limit_selections_addition(self):
        with self.assertRaises(TypeError):
            self.sky_region.limit_selections["RA"] = Selection()
