import unittest

from lsst.sims.ocs.configuration.science import GalacticPlane
from SALPY_scheduler import scheduler_areaDistPropConfigC

class GalacticPlaneTest(unittest.TestCase):

    def setUp(self):
        self.prop = GalacticPlane()

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.prop.sky_region.selections), 1)
        self.assertEqual(self.prop.sky_region.selections[0].limit_type, "GP")
        self.assertEqual(self.prop.sky_region.selections[0].bounds_limit, 90.0)
        self.assertIsNone(self.prop.sky_exclusion.selections)
        self.assertEqual(self.prop.sky_constraints.max_airmass, 2.5)
        self.assertEqual(self.prop.sky_nightly_bounds.twilight_boundary, -12.0)
        self.assertEqual(len(self.prop.filters), 6)
        self.assertEqual(self.prop.filters['u'].num_visits, 30)
        self.assertEqual(self.prop.filters['u'].bright_limit, 20.8)
        self.assertEqual(self.prop.filters['i'].num_visits, 30.0)
        self.assertEqual(self.prop.filters['i'].bright_limit, 19.5)
        self.assertFalse(self.prop.scheduling.accept_serendipity)
        self.assertFalse(self.prop.scheduling.accept_consecutive_visits)

    def test_set_topic(self):
        in_topic = scheduler_areaDistPropConfigC()
        out_topic = self.prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "GalacticPlane")
        self.assertEqual(out_topic.num_region_selections, 1)
        self.assertEqual(out_topic.num_exclusion_selections, 0)
        self.assertEqual(out_topic.region_minimums[0], 0.0)
        self.assertEqual(out_topic.num_filters, 6)
        self.assertEqual(out_topic.max_seeing[5], 2.0)
        self.assertEqual(out_topic.num_filter_exposures[5], 2)
        self.assertEqual(out_topic.exposures[11], 15.0)
