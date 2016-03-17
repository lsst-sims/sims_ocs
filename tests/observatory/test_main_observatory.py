import logging
import math
import unittest

from lsst.sims.ocs.kernel import TimeHandler
from lsst.sims.ocs.observatory import MainObservatory
from ..database import topic_helpers

class MainObservatoryTest(unittest.TestCase):

    def setUp(self):
        logging.getLogger().setLevel(logging.WARN)
        self.observatory = MainObservatory()

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
        self.assertEqual(len(self.observatory.model.prerequisites["telsettle"]), 2)

    def test_slew(self):
        self.observatory.configure()
        target = topic_helpers.target
        slew_time = self.observatory.slew(target)
        self.assertEqual(slew_time, 6.0)
        self.assertEqual(self.observatory.slew_count, 1)

    def test_observe(self):
        self.observatory.configure()
        target = topic_helpers.target
        observation = topic_helpers.observation_topic
        # Make it so initial timestamp is 0
        time_handler = TimeHandler("1970-01-01")
        self.observatory.observe(time_handler, target, observation)
        self.assertEqual(observation.observationId, 1)
        self.assertEqual(observation.observationTime, 6.0)
