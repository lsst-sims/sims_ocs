import unittest

from lsst.sims.ocs.configuration.science import NorthEclipticSpur
from SALPY_scheduler import scheduler_generalPropConfigC

class NorthEclipticSpurTest(unittest.TestCase):

    def setUp(self):
        self.prop = NorthEclipticSpur()
        self.time_interval = 30 * 60

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.prop.sky_region.selections), 2)
        self.assertEqual(self.prop.sky_region.selections[0].limit_type, "EB")
        self.assertEqual(self.prop.sky_region.selections[0].minimum_limit, -30.0)
        self.assertEqual(self.prop.sky_region.selections[1].limit_type, "Dec")
        self.assertEqual(self.prop.sky_region.selections[1].minimum_limit, 2.8)
        self.assertEqual(len(self.prop.sky_exclusion.selections), 0)
        self.assertEqual(self.prop.sky_constraints.max_airmass, 2.5)
        self.assertEqual(self.prop.sky_constraints.max_cloud, 0.7)
        self.assertEqual(self.prop.sky_nightly_bounds.twilight_boundary, -12.0)
        self.assertEqual(len(self.prop.filters), 4)
        self.assertEqual(self.prop.filters['g'].num_visits, 40)
        self.assertEqual(self.prop.filters['g'].num_grouped_visits, 2)
        self.assertEqual(self.prop.filters['g'].bright_limit, 21.0)
        self.assertEqual(self.prop.filters['g'].max_seeing, 2.0)
        self.assertEqual(self.prop.filters['i'].num_visits, 92)
        self.assertEqual(self.prop.filters['i'].bright_limit, 19.5)
        self.assertFalse(self.prop.scheduling.accept_serendipity)
        self.assertFalse(self.prop.scheduling.accept_consecutive_visits)
        self.assertEqual(self.prop.scheduling.airmass_bonus, 0.5)
        self.assertTrue(self.prop.scheduling.restrict_grouped_visits)
        self.assertEqual(self.prop.scheduling.time_interval, self.time_interval)
        self.assertEqual(self.prop.scheduling.time_window_start, 0.5)
        self.assertEqual(self.prop.scheduling.time_window_max, 1.0)
        self.assertEqual(self.prop.scheduling.time_window_end, 2.0)
        self.assertEqual(self.prop.scheduling.time_weight, 1.0)

    def test_set_topic(self):
        in_topic = scheduler_generalPropConfigC()
        out_topic = self.prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "NorthEclipticSpur")
        self.assertEqual(out_topic.num_region_selections, 2)
        self.assertEqual(out_topic.num_exclusion_selections, 0)
        self.assertNotEqual(out_topic.region_minimums[1], 0.0)
        self.assertEqual(out_topic.region_combiners, "and")
        self.assertEqual(out_topic.num_filters, 4)
        self.assertEqual(out_topic.max_seeing[1], 2.0)
        self.assertEqual(out_topic.num_filter_exposures[1], 2)
        self.assertEqual(out_topic.num_grouped_visits[1], 2)
        self.assertEqual(out_topic.exposures[3], 15.0)
        self.assertEqual(out_topic.max_cloud, 0.7)
        self.assertEqual(out_topic.airmass_bonus, 0.5)
        self.assertTrue(out_topic.restrict_grouped_visits)
        self.assertEqual(out_topic.time_interval, self.time_interval)
        self.assertEqual(out_topic.time_window_end, 2.0)
