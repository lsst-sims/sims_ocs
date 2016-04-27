import logging
import math
import unittest

from SALPY_scheduler import scheduler_observationTestC

from lsst.sims.ocs.kernel import TimeHandler
from lsst.sims.ocs.observatory import MainObservatory

from tests.database import topic_helpers

class MainObservatoryTest(unittest.TestCase):

    def setUp(self):
        self.truth_slew_time = 56.347699999734026
        logging.getLogger().setLevel(logging.WARN)
        self.observatory = MainObservatory()

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.observatory.log)
        self.assertEqual(len(self.observatory.param_dict), 0)
        self.assertEqual(self.observatory.model.location.latitude_rad, math.radians(-30.2444))
        self.assertFalse(self.observatory.model.parkState.tracking)
        self.assertEqual(len(self.observatory.model.currentState.mountedfilters), 5)
        self.assertEqual(self.observatory.exposures_made, 0)
        self.assertIsNone(self.observatory.exposure_list)

    def test_information_after_configuration(self):
        self.observatory.configure()
        self.assertEqual(len(self.observatory.param_dict), 6)
        self.assertEqual(self.observatory.model.TelAz_MaxSpeed_rad, math.radians(7.0))
        self.assertEqual(self.observatory.model.parkState.alt_rad, math.radians(86.5))
        self.assertFalse(self.observatory.model.Rotator_FollowSky)
        self.assertEqual(len(self.observatory.model.prerequisites["telsettle"]), 2)

    def test_slew(self):
        self.observatory.configure()
        target = topic_helpers.target
        self.assertEqual(self.observatory.slew_count, 0)
        slew_time, slew_history = self.observatory.slew(target)
        self.assertEqual(slew_time[0], self.truth_slew_time)
        self.assertEqual(self.observatory.slew_count, 1)
        self.assertEqual(slew_history.slewCount, 1)
        self.assertEqual(slew_history.ObsHistory_observationId, 0)
        self.assertEqual(slew_history.slewDistance, 3.1621331347877555)

    def test_observe(self):
        self.observatory.configure()
        target = topic_helpers.target
        observation = scheduler_observationTestC()
        # Make it so initial timestamp is 0
        time_handler = TimeHandler("1970-01-01")
        slew_history, exposures = self.observatory.observe(time_handler, target, observation)
        self.assertEqual(observation.observationId, 1)
        self.assertEqual(observation.exposure_times[1], 15.0)
        self.assertAlmostEqual(observation.observationTime, self.truth_slew_time, delta=1e-4)
        self.assertIsNotNone(slew_history)
        self.assertEqual(self.observatory.exposures_made, 2)
        self.assertEqual(len(exposures), self.observatory.exposures_made)

    def test_visit_time(self):
        self.observatory.configure()
        target = topic_helpers.target
        visit_time = self.observatory.calculate_visit_time(target)
        self.assertEqual(visit_time[0], 34.0)
