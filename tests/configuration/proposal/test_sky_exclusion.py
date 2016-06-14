import unittest

from lsst.sims.ocs.configuration.proposal import Selection
from lsst.sims.ocs.configuration.proposal import SkyExclusion

class SkyExclusionTest(unittest.TestCase):

    def setUp(self):
        self.sky_exclusion = SkyExclusion()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sky_exclusion.dec_window, 90.0)
        self.assertIsNone(self.sky_exclusion.exclusion_selections)

    def test_exclusion_selections_assignment(self):
        self.sky_exclusion.exclusion_selections = {0: Selection()}
        self.assertIsNotNone(self.sky_exclusion.exclusion_selections)
        self.assertEqual(len(self.sky_exclusion.exclusion_selections), 1)

    def test_exclusion_selections_addition(self):
        with self.assertRaises(TypeError):
            self.sky_exclusion.exclusion_selections[0] = Selection()
