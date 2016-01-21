import math
import unittest

from lsst.sims.ocs.observatory.lsst_observatory import LsstObservatory

class LsstObservatoryTest(unittest.TestCase):

    def setUp(self):
        self.observatory = LsstObservatory()

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.observatory.log)
        self.assertEqual(len(self.observatory.param_dict), 0)
        self.assertEqual(self.observatory.model.location.latitude_rad, 0.0)
        self.assertFalse(self.observatory.model.parkState.tracking)
        self.assertEqual(len(self.observatory.model.currentState.mountedfilters), 5)

    def test_information_after_configuration(self):
        self.observatory.configure()
        self.assertEqual(len(self.observatory.param_dict), 7)
        self.assertEqual(self.observatory.model.location.latitude_rad, math.radians(-30.2444))
        self.assertEqual(self.observatory.model.TelAz_MaxSpeed_rad, math.radians(7.0))
        self.assertEqual(self.observatory.model.parkState.alt_rad, math.radians(86.5))
        self.assertFalse(self.observatory.model.Rotator_FollowSky)
        self.assertEqual(len(self.observatory.model.prerequisites["TelSettle"]), 2)
