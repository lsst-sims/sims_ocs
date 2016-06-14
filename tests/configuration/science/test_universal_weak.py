import unittest

from lsst.sims.ocs.configuration.science import UniversalWeak
from SALPY_scheduler import scheduler_areaDistPropConfigC

class UniversalWeakTest(unittest.TestCase):

    def setUp(self):
        self.prop = UniversalWeak()

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.prop.sky_region.region_selections), 1)
        self.assertEqual(self.prop.sky_region.region_selections[0].limit_type, "Dec")
        self.assertEqual(self.prop.sky_region.region_selections[0].minimum_limit, -62.5)
        self.assertEqual(len(self.prop.filters), 6)
        self.assertEqual(self.prop.filters['u'].num_visits, 75)
        self.assertEqual(self.prop.filters['u'].bright_limit, 21.3)
        self.assertEqual(self.prop.filters['i'].num_visits, 240)
        self.assertEqual(self.prop.filters['i'].bright_limit, 19.5)
        self.assertFalse(self.prop.scheduling.accept_serendipity)
        self.assertFalse(self.prop.scheduling.accept_consecutive_visits)

    def test_set_topic(self):
        in_topic = scheduler_areaDistPropConfigC()
        out_topic = self.prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "UniversalWeak")
        self.assertEqual(out_topic.num_region_selections, 1)
        self.assertEqual(out_topic.region_minimums[1], 0.0)
        self.assertEqual(out_topic.num_filters, 6)
        self.assertEqual(out_topic.max_seeing[5], 1.5)
        self.assertEqual(out_topic.num_filter_exposures[5], 2)
        self.assertEqual(out_topic.exposures[11], 15.0)
