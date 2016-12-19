import math
import unittest

from lsst.sims.ocs.configuration.proposal import General
from SALPY_scheduler import scheduler_generalPropConfigC

from tests.configuration.proposal.basic_proposal1 import BasicProposal1
from tests.configuration.proposal.basic_proposal2 import BasicProposal2
from tests.configuration.proposal.basic_proposal3 import BasicProposal3
from tests.configuration.proposal.basic_proposal4 import BasicProposal4

class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.ad = General()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.ad.name)
        self.assertIsNotNone(self.ad.sky_region)
        self.assertIsNotNone(self.ad.sky_exclusion)
        self.assertIsNotNone(self.ad.sky_nightly_bounds)
        self.assertIsNotNone(self.ad.sky_constraints)
        self.assertIsNone(self.ad.filters)
        self.assertIsNotNone(self.ad.scheduling)

    def test_default_set_topic(self):
        in_topic = scheduler_generalPropConfigC()
        out_topic = self.ad.set_topic(in_topic)
        self.assertEqual(out_topic.name, "None")

    def test_specific_set_topic(self):
        ad = BasicProposal1()
        in_topic = scheduler_generalPropConfigC()
        self.assertTrue(hasattr(in_topic, "max_airmass"))
        out_topic = ad.set_topic(in_topic)
        self.assertEqual(out_topic.name, "BasicProposal1")
        self.assertEqual(out_topic.max_airmass, 2.5)
        self.assertEqual(out_topic.num_region_selections, 2)
        self.assertEqual(out_topic.region_types.split(',')[1], "RA")
        self.assertTrue(math.isnan(out_topic.region_bounds[1]))
        self.assertEqual(len(out_topic.region_combiners.split(',')), 1)
        self.assertEqual(out_topic.num_exclusion_selections, 1)
        self.assertEqual(out_topic.exclusion_types.split(',')[0], "GP")
        self.assertEqual(out_topic.exclusion_bounds[0], 90.0)
        self.assertEqual(out_topic.num_filters, 6)
        self.assertEqual(len(out_topic.filter_names.split(',')), 6)
        self.assertEqual(out_topic.num_grouped_visits[0], 1)
        self.assertTrue(out_topic.restrict_grouped_visits)
        self.assertEqual(out_topic.time_interval, 0.0)
        self.assertEqual(out_topic.time_window_start, 0.0)
        self.assertEqual(out_topic.time_window_max, 0.0)
        self.assertEqual(out_topic.time_window_end, 0.0)

    def test_another_specific_set_topic(self):
        ad = BasicProposal2()
        in_topic = scheduler_generalPropConfigC()
        out_topic = ad.set_topic(in_topic)
        self.assertEqual(out_topic.name, "BasicProposal2")
        self.assertEqual(out_topic.num_region_selections, 2)
        self.assertEqual(out_topic.num_exclusion_selections, 0)
        self.assertEqual(out_topic.num_filters, 3)

    def test_a_hybrid_proposal_set_topic(self):
        ad = BasicProposal3()
        in_topic = scheduler_generalPropConfigC()
        out_topic = ad.set_topic(in_topic)
        self.assertEqual(out_topic.name, "BasicProposal3")
        self.assertEqual(out_topic.num_filters, 4)
        filter_names = out_topic.filter_names.split(',')
        idx1 = filter_names.index('u')
        idx2 = filter_names.index('g')
        self.assertEqual(out_topic.num_grouped_visits[idx1], 1)
        self.assertEqual(out_topic.num_grouped_visits[idx2], 2)
        self.assertFalse(out_topic.restrict_grouped_visits)
        self.assertEqual(out_topic.time_interval, 30 * 60)
        self.assertEqual(out_topic.time_window_start, -0.5)
        self.assertEqual(out_topic.time_window_max, 0.5)
        self.assertEqual(out_topic.time_window_end, 1.0)

    def test_a_time_ordered_proposal_set_topic(self):
        gen = BasicProposal4()
        in_topic = scheduler_generalPropConfigC()
        out_topic = gen.set_topic(in_topic)
        self.assertEqual(out_topic.name, "BasicProposal4")
        self.assertEqual(out_topic.num_region_selections, 2)
        self.assertEqual(out_topic.num_time_ranges, 2)
        self.assertEqual(out_topic.time_range_starts[0], 1)
        self.assertEqual(out_topic.time_range_ends[0], 1825)
        self.assertEqual(out_topic.time_range_starts[1], 1826)
        self.assertEqual(out_topic.time_range_ends[1], 3650)
        self.assertEqual(out_topic.num_selection_mappings[0], 1)
        self.assertEqual(out_topic.num_selection_mappings[1], 1)
        self.assertEqual(out_topic.selection_mappings[0], 0)
        self.assertEqual(out_topic.selection_mappings[1], 1)
