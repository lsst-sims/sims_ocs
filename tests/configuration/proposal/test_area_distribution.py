import unittest

from lsst.sims.ocs.configuration.proposal import AreaDistribution
from SALPY_scheduler import scheduler_areaDistPropConfigC

class AreaDistributionTest(unittest.TestCase):

    def setUp(self):
        self.ad = AreaDistribution()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.ad.name)
        self.assertIsNotNone(self.ad.sky_region)
        self.assertIsNone(self.ad.filters)
        self.assertIsNotNone(self.ad.scheduling)

    def test_set_topic(self):
        in_topic = scheduler_areaDistPropConfigC()
        out_topic = self.ad.set_topic(in_topic)
        self.assertEqual(out_topic.name, "None")
