import unittest

from lsst.ts.schedulerConfig.proposal import BaseSequence

class BaseSequenceTest(unittest.TestCase):

    def setUp(self):
        self.base_seq = BaseSequence()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.base_seq.num_events, 0)
        self.assertEqual(self.base_seq.num_max_missed, 0)
        self.assertEqual(self.base_seq.time_interval, 0.0)
        self.assertEqual(self.base_seq.time_window_start, 0.0)
        self.assertEqual(self.base_seq.time_window_max, 0.0)
        self.assertEqual(self.base_seq.time_window_end, 0.0)
        self.assertEqual(self.base_seq.time_weight, 0.0)
