import unittest

from lsst.ts.schedulerConfig import ScienceProposals
from tests.helpers import GEN_PROPS, NUM_GEN_PROPS, NUM_SEQ_PROPS, SEQ_PROPS

class ScienceProposalsTest(unittest.TestCase):

    def setUp(self):
        self.sci_props = ScienceProposals()

    def test_basic_information_from_creation(self):
        self.assertIsNotNone(self.sci_props.general_props)
        self.assertEqual(len(self.sci_props.general_props), NUM_GEN_PROPS)
        self.assertListEqual(self.sci_props.general_proposals, GEN_PROPS)
        self.assertIsNotNone(self.sci_props.sequence_props)
        self.assertEqual(len(self.sci_props.sequence_props), NUM_SEQ_PROPS)
        self.assertListEqual(self.sci_props.sequence_proposals, SEQ_PROPS)
