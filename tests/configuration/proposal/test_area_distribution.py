import unittest

from lsst.sims.ocs.configuration.proposal import AreaDistribution

class AreaDistributionTest(unittest.TestCase):

    def setUp(self):
        self.ad = AreaDistribution()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.ad.name)
        self.assertIsNotNone(self.ad.sky_region)
        self.assertIsNone(self.ad.filters)
