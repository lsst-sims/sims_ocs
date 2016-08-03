import unittest

from lsst.sims.ocs.configuration import ScienceProposals
from tests.helpers import AREA_DIST_PROPS, NUM_AREA_DIST_PROPS

class ScienceProposalsTest(unittest.TestCase):

    def setUp(self):
        self.sci_props = ScienceProposals()

    def test_basic_information_from_creation(self):
        self.assertIsNotNone(self.sci_props.area_dist_props)
        self.assertEqual(len(self.sci_props.area_dist_props), NUM_AREA_DIST_PROPS)
        self.assertEqual(self.sci_props.ad_proposals, AREA_DIST_PROPS)
