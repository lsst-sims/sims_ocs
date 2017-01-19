import unittest

from lsst.sims.ocs.configuration.proposal import Sequence
from SALPY_scheduler import scheduler_sequencePropConfigC

from tests.configuration.proposal.basic_proposal5 import BasicProposal5

class SequenceTest(unittest.TestCase):

    def setUp(self):
        self.prop = Sequence()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.prop.name)
        self.assertIsNotNone(self.prop.sky_user_regions)
        self.assertIsNone(self.prop.sub_sequences)
        self.assertIsNotNone(self.prop.sky_exclusion)
        self.assertIsNotNone(self.prop.sky_nightly_bounds)
        self.assertIsNotNone(self.prop.sky_constraints)
        self.assertIsNotNone(self.prop.scheduling)

    def test_default_set_topic(self):
        in_topic = scheduler_sequencePropConfigC()
        out_topic = self.prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "None")

    def test_specific_set_topic(self):
        prop = BasicProposal5()
        in_topic = scheduler_sequencePropConfigC()
        self.assertTrue(hasattr(in_topic, "max_airmass"))
        out_topic = prop.set_topic(in_topic)
        self.assertEqual(out_topic.name, "BasicProposal5")
        self.assertEqual(out_topic.num_user_regions, 3)
        self.assertEqual(out_topic.user_region_ids[1], 1486)
        self.assertEqual(out_topic.max_airmass, 2.5)
        self.assertEqual(out_topic.dec_window, 90.0)
        nss = 2
        self.assertEqual(out_topic.num_sub_sequences, nss)
        self.assertEqual(out_topic.sub_sequence_names, 'Only_GR,Only_IZ')
        self.assertEqual(out_topic.sub_sequence_filters, 'g,r,i,z')
        self.assertListEqual(list(out_topic.num_sub_sequence_filters)[:nss], [2, 2])
        self.assertEqual(out_topic.num_sub_sequence_filters[nss], 0)
        self.assertListEqual(list(out_topic.num_sub_sequence_filter_visits)[:nss * 2], [25, 30, 35, 10])
        self.assertListEqual(list(out_topic.num_sub_sequence_events)[:nss], [20, 25])
        self.assertListEqual(list(out_topic.num_sub_sequence_max_missed)[:nss], [5, 10])
        self.assertListEqual(list(out_topic.sub_sequence_time_intervals)[:nss], [259200, 432000])
        self.assertListEqual(list(out_topic.sub_sequence_time_window_starts)[:nss], [0.0, 0.0])
        self.assertListEqual(list(out_topic.sub_sequence_time_window_maximums)[:nss], [1.0, 1.0])
        self.assertListEqual(list(out_topic.sub_sequence_time_window_ends)[:nss], [2.0, 2.0])
        self.assertListEqual(list(out_topic.sub_sequence_time_weights)[:nss], [1.0, 1.0])
        self.assertTrue(out_topic.accept_consecutive_visits)
        self.assertEqual(out_topic.num_filters, 4)
        filter_names = out_topic.filter_names.split(',')
        self.assertEqual(len(filter_names), 4)
        idx = filter_names.index('g')
        self.assertEqual(out_topic.max_seeing[idx], 1.5)
        self.assertEqual(out_topic.bright_limit[idx], 21.0)
        self.assertEqual(out_topic.num_filter_exposures[idx], 2)
