import unittest

from lsst.sims.ocs.configuration.science import DeepDrillingCosmology1
from SALPY_scheduler import scheduler_sequencePropConfigC

class DeepDrillingCosmology1Test(unittest.TestCase):

    def setUp(self):
        self.prop = DeepDrillingCosmology1()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.prop.name, "DeepDrillingCosmology1")
        self.assertListEqual(list(self.prop.sky_user_regions),
                             [290, 744, 1427, 2412, 2786])
        self.assertEqual(self.prop.sky_constraints.max_airmass, 1.5)
        self.assertEqual(self.prop.sky_constraints.max_cloud, 0.7)
        self.assertEqual(self.prop.sky_nightly_bounds.twilight_boundary, -12.0)
        self.assertTrue(self.prop.scheduling.accept_consecutive_visits)
        self.assertEqual(self.prop.filters['u'].max_seeing, 1.5)
        self.assertEqual(self.prop.filters['g'].bright_limit, 19.5)
        self.assertEqual(self.prop.filters['r'].bright_limit, 19.5)
        self.assertEqual(self.prop.filters['z'].bright_limit, 17.5)
        self.assertEqual(self.prop.filters['y'].dark_limit, 30.0)

    def test_set_topic(self):
        in_topic = scheduler_sequencePropConfigC()
        out_topic = self.prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "DeepDrillingCosmology1")
        self.assertEqual(out_topic.num_user_regions, 5)
        self.assertEqual(out_topic.user_region_ids[4], 2786)
        self.assertEqual(out_topic.num_filters, 6)
        filter_names = out_topic.filter_names.split(',')
        idx1 = filter_names.index('g')
        idx2 = filter_names.index('y')
        self.assertEqual(out_topic.bright_limit[idx1], 19.5)
        self.assertEqual(out_topic.dark_limit[idx2], 30.0)
