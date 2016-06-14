import unittest

from lsst.sims.ocs.configuration.proposal import Selection
from lsst.sims.ocs.configuration.proposal import SkyRegion

class SkyRegionTest(unittest.TestCase):

    def setUp(self):
        self.sky_region = SkyRegion()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.sky_region.region_selections)
        self.assertIsNotNone(self.sky_region.region_combiners)

    def test_region_selections_assignment(self):
        self.sky_region.region_selections = {0: Selection()}
        self.assertIsNotNone(self.sky_region.region_selections)
        self.assertEqual(len(self.sky_region.region_selections), 1)

    def test_region_selections_addition(self):
        with self.assertRaises(TypeError):
            self.sky_region.region_selections[0] = Selection()
