import unittest

from lsst.sims.ocs.configuration.proposal import Sequence

class SequenceTest(unittest.TestCase):

    def setUp(self):
        self.prop = Sequence()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.prop.name)
        self.assertIsNotNone(self.prop.sky_user_regions)
        self.assertIsNotNone(self.prop.sky_nightly_bounds)
        self.assertIsNotNone(self.prop.sky_constraints)
        self.assertIsNotNone(self.prop.scheduling)
