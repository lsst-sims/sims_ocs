import unittest

from lsst.sims.ocs.configuration.proposal import GalacticExclusion

class GalacticExclusionTest(unittest.TestCase):

    def setUp(self):
        self.gal_ex = GalacticExclusion()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.gal_ex.taper_l, 2.0)
        self.assertEqual(self.gal_ex.taper_b, 180.0)
        self.assertEqual(self.gal_ex.peak_l, 20.0)
