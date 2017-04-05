import unittest

from lsst.sims.ocs.configuration.proposal import SequenceScheduling

class SequenceSchedulingTest(unittest.TestCase):

    def setUp(self):
        self.sched = SequenceScheduling()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sched.max_num_targets, 100)
        self.assertTrue(self.sched.accept_consecutive_visits)
        self.assertTrue(self.sched.accept_serendipity)
        self.assertEqual(self.sched.airmass_bonus, 0.5)
        self.assertTrue(self.sched.restart_lost_sequences)
        self.assertTrue(self.sched.restart_complete_sequences)
