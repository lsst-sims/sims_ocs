import unittest

from lsst.sims.ocs.observatory.lsst_observatory import LsstObservatory

class LsstObservatoryTest(unittest.TestCase):

    def setUp(self):
        self.observatory = LsstObservatory()

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.observatory.log)
