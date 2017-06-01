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
        self.assertEqual(self.prop.sky_constraints.min_distance_moon, 30.0)
        self.assertEqual(len(self.prop.sub_sequences), 2)
        self.assertEqual(self.prop.sub_sequences[1].name, "u-band")
        self.assertListEqual(list(self.prop.sub_sequences[0].filters), ['r', 'g', 'i', 'z', 'y'])
        self.assertListEqual(list(self.prop.sub_sequences[1].visits_per_filter), [20])
        self.assertEqual(self.prop.sub_sequences[0].num_events, 27)
        self.assertEqual(self.prop.sub_sequences[1].num_max_missed, 0)
        self.assertEqual(self.prop.sub_sequences[0].time_interval, 259200)
        self.assertEqual(self.prop.sub_sequences[1].time_window_start, 0.8)
        self.assertEqual(self.prop.sub_sequences[0].time_window_max, 1.0)
        self.assertEqual(self.prop.sub_sequences[1].time_window_end, 1.4)
        self.assertEqual(self.prop.sub_sequences[0].time_weight, 1.0)
        self.assertEqual(len(self.prop.master_sub_sequences), 0)
        self.assertTrue(self.prop.scheduling.accept_consecutive_visits)
        self.assertTrue(self.prop.scheduling.restart_lost_sequences)
        self.assertTrue(self.prop.scheduling.restart_complete_sequences)
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
        self.assertTrue(out_topic.exclude_planets)
        self.assertEqual(out_topic.num_sub_sequences, 2)
        self.assertEqual(out_topic.sub_sequence_names, "main,u-band")
        nss = 2
        self.assertListEqual(list(out_topic.num_sub_sequence_filters)[:nss], [5, 1])
        self.assertEqual(out_topic.sub_sequence_filters, 'r,g,i,z,y,u')
        self.assertEqual(out_topic.num_sub_sequence_filters[nss], 0)
        self.assertListEqual(list(out_topic.num_sub_sequence_filter_visits)[:nss * 3],
                             [20, 10, 20, 26, 20, 20])
        self.assertListEqual(list(out_topic.num_sub_sequence_events)[:nss], [27, 7])
        self.assertListEqual(list(out_topic.num_sub_sequence_max_missed)[:nss], [0, 0])
        self.assertListEqual(list(out_topic.sub_sequence_time_intervals)[:nss], [259200, 86400])
        self.assertListEqual(list(out_topic.sub_sequence_time_window_starts)[:nss], [0.8, 0.8])
        self.assertListEqual(list(out_topic.sub_sequence_time_window_maximums)[:nss], [1.0, 1.0])
        self.assertListEqual(list(out_topic.sub_sequence_time_window_ends)[:nss], [1.4, 1.4])
        self.assertListEqual(list(out_topic.sub_sequence_time_weights)[:nss], [1.0, 1.0])
        self.assertEqual(out_topic.num_master_sub_sequences, 0)
        self.assertTrue(out_topic.restart_lost_sequences)
        self.assertTrue(out_topic.restart_complete_sequences)
        self.assertEqual(out_topic.num_filters, 6)
        filter_names = out_topic.filter_names.split(',')
        idx1 = filter_names.index('g')
        idx2 = filter_names.index('y')
        self.assertEqual(out_topic.bright_limit[idx1], 19.5)
        self.assertEqual(out_topic.dark_limit[idx2], 30.0)

    def test_proposal_fields(self):
        ids = self.prop.proposal_fields()
        self.assertEqual(len(ids), 5)
