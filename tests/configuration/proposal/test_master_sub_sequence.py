import unittest

from lsst.ts.schedulerConfig.proposal import MasterSubSequence

class MasterSubSequenceTest(unittest.TestCase):

    def setUp(self):
        self.master_sub_seq = MasterSubSequence()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.master_sub_seq.name)
        self.assertIsNone(self.master_sub_seq.sub_sequences)
