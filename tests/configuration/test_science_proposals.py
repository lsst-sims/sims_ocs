import unittest

from lsst.sims.ocs.configuration import ScienceProposals
from tests.helpers import GEN_PROPS, NUM_GEN_PROPS

class ScienceProposalsTest(unittest.TestCase):

    def setUp(self):
        self.sci_props = ScienceProposals()

    def test_basic_information_from_creation(self):
        self.assertIsNotNone(self.sci_props.gen_props)
        self.assertEqual(len(self.sci_props.gen_props), NUM_GEN_PROPS)
        self.assertListEqual(self.sci_props.gen_proposals, GEN_PROPS)
