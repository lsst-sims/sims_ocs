import unittest

from lsst.ts.schedulerConfig.proposal import Selection
from lsst.ts.schedulerConfig.proposal import SkyExclusion

class SkyExclusionTest(unittest.TestCase):

    def setUp(self):
        self.sky_exclusion = SkyExclusion()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sky_exclusion.dec_window, 90.0)
        self.assertIsNotNone(self.sky_exclusion.selections)

    def test_selections_assignment(self):
        self.sky_exclusion.selections = {0: Selection()}
        self.assertIsNotNone(self.sky_exclusion.selections)
        self.assertEqual(len(self.sky_exclusion.selections), 1)
