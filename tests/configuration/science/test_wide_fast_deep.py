import unittest

from lsst.sims.ocs.configuration.science import WideFastDeep
from SALPY_scheduler import scheduler_generalPropConfigC

class WideFastDeepTest(unittest.TestCase):

    def setUp(self):
        self.prop = WideFastDeep()
        self.time_interval = 30 * 60

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.prop.sky_region.selections), 1)
        self.assertEqual(self.prop.sky_region.selections[0].limit_type, "Dec")
        self.assertEqual(self.prop.sky_region.selections[0].minimum_limit, -62.5)
        self.assertEqual(len(self.prop.sky_exclusion.selections), 1)
        self.assertEqual(self.prop.sky_exclusion.selections[0].limit_type, "GP")
        self.assertEqual(self.prop.sky_exclusion.selections[0].minimum_limit, 0.0)
        self.assertEqual(self.prop.sky_constraints.max_airmass, 1.5)
        self.assertEqual(self.prop.sky_nightly_bounds.twilight_boundary, -12.0)
        self.assertEqual(len(self.prop.filters), 6)
        self.assertEqual(self.prop.filters['u'].num_visits, 75)
        self.assertEqual(self.prop.filters['u'].bright_limit, 21.3)
        self.assertEqual(self.prop.filters['u'].num_grouped_visits, 1)
        self.assertEqual(self.prop.filters['i'].num_visits, 240)
        self.assertEqual(self.prop.filters['i'].bright_limit, 19.5)
        self.assertEqual(self.prop.filters['i'].num_grouped_visits, 2)
        self.assertFalse(self.prop.scheduling.accept_serendipity)
        self.assertFalse(self.prop.scheduling.accept_consecutive_visits)
        self.assertTrue(self.prop.scheduling.restrict_grouped_visits)
        self.assertEqual(self.prop.scheduling.time_interval, self.time_interval)
        self.assertEqual(self.prop.scheduling.time_window_start, 0.5)
        self.assertEqual(self.prop.scheduling.time_window_max, 1.0)
        self.assertEqual(self.prop.scheduling.time_window_end, 2.0)
        self.assertEqual(self.prop.scheduling.time_weight, 1.0)

    def test_set_topic(self):
        in_topic = scheduler_generalPropConfigC()
        out_topic = self.prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "WideFastDeep")
        self.assertEqual(out_topic.num_region_selections, 1)
        self.assertEqual(out_topic.num_exclusion_selections, 1)
        self.assertEqual(out_topic.region_minimums[1], 0.0)
        self.assertEqual(out_topic.num_filters, 6)
        self.assertEqual(out_topic.max_seeing[5], 1.5)
        self.assertEqual(out_topic.num_filter_exposures[5], 2)
        self.assertEqual(out_topic.exposures[11], 15.0)
        self.assertEqual(out_topic.num_grouped_visits[1], 2)
        self.assertEqual(out_topic.exposures[3], 15.0)
        self.assertEqual(out_topic.max_cloud, 0.7)
        self.assertEqual(out_topic.airmass_bonus, 0.5)
        self.assertTrue(out_topic.restrict_grouped_visits)
        self.assertEqual(out_topic.time_interval, self.time_interval)
        self.assertEqual(out_topic.time_window_end, 2.0)
