import unittest

from lsst.ts.schedulerConfig.proposal import GeneralScheduling

class GeneralSchedulingTest(unittest.TestCase):

    def setUp(self):
        self.sched = GeneralScheduling()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sched.max_num_targets, 100)
        self.assertTrue(self.sched.accept_consecutive_visits)
        self.assertTrue(self.sched.accept_serendipity)
        self.assertEqual(self.sched.airmass_bonus, 0.5)
        self.assertTrue(self.sched.restrict_grouped_visits)
        self.assertEqual(self.sched.time_interval, 0.0)
        self.assertEqual(self.sched.time_window_start, 0.0)
        self.assertEqual(self.sched.time_window_max, 0.0)
        self.assertEqual(self.sched.time_window_end, 0.0)
        self.assertEqual(self.sched.time_weight, 0.0)
