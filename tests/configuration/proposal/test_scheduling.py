import unittest

from lsst.ts.schedulerConfig.proposal import Scheduling

class SchedulingTest(unittest.TestCase):

    def setUp(self):
        self.sched = Scheduling()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sched.max_num_targets, 100)
        self.assertTrue(self.sched.accept_consecutive_visits)
        self.assertTrue(self.sched.accept_serendipity)
        self.assertEqual(self.sched.airmass_bonus, 0.5)
        self.assertEqual(self.sched.hour_angle_bonus, 0.0)
        self.assertEqual(self.sched.hour_angle_max, 6.0)
