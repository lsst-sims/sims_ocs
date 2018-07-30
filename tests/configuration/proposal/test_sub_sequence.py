import unittest

from lsst.ts.schedulerConfig.proposal import SubSequence

class SubSequenceTest(unittest.TestCase):

    def setUp(self):
        self.sub_seq = SubSequence()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.sub_seq.name)
        self.assertListEqual(list(self.sub_seq.filters), [])
        self.assertListEqual(list(self.sub_seq.visits_per_filter), [])

    def test_filter_list_rep(self):
        sub_seq = SubSequence()
        sub_seq.filters = ['g', 'r', 'i']
        self.assertEqual(sub_seq.get_filter_string(), 'g,r,i')
