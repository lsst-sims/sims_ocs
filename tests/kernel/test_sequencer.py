import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.kernel.sequencer import Sequencer
from lsst.sims.ocs.kernel.time_handler import TimeHandler
from lsst.sims.ocs.sal.sal_manager import SalManager

class SequencerTest(unittest.TestCase):

    def setUp(self):
        self.seq = Sequencer()

    def initialize_sequencer(self):
        self.sal = SalManager()
        self.sal.initialize()
        self.seq.initialize(self.sal)

    def create_objects(self):
        target = self.sal.set_subscribe_topic("targetTest")
        # Set some meaningful information
        target.targetId = 10
        target.fieldId = 300
        target.filter = "i"
        target.ra = 0.4244
        target.dec = -0.5314
        target.num_exposures = 2

        # Make it so initial timestamp is 0
        time_handler = TimeHandler("1970-01-01")

        return target, time_handler

    def test_basic_information_after_creation(self):
        self.assertEqual(self.seq.observations_made, 0)
        self.assertEqual(self.seq.targets_received, 0)
        self.assertIsNone(self.seq.observation)
        self.assertIsNotNone(self.seq.observatory_model)

    @mock.patch("lsst.sims.ocs.observatory.main_observatory.MainObservatory.configure")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_initialization(self, mock_sal_telemetry_pub, mock_main_observatory_configure):
        self.initialize_sequencer()
        self.assertIsNotNone(self.seq.observation)
        self.assertEqual(self.seq.observation.observationId, 0)
        self.assertTrue(mock_sal_telemetry_pub.called)
        self.assertTrue(mock_main_observatory_configure.called)

    @mock.patch("logging.Logger.info")
    def test_finalization(self, mock_logger_info):
        self.seq.finalize()
        self.assertEqual(mock_logger_info.call_count, 2)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_observe_target(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()

        observation, slew_history = self.seq.observe_target(target, time_handler)

        self.assertEqual(observation.observationTime, time_handler.initial_timestamp + 140.0)
        self.assertEqual(observation.targetId, target.targetId)
        self.assertEqual(self.seq.targets_received, 1)
        self.assertEqual(self.seq.observations_made, 1)
        self.assertIsNotNone(slew_history)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_end_of_night(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()

        # Don't care about outputs
        self.seq.observe_target(target, time_handler)
        self.seq.end_of_night()

        obs_current_state = self.seq.observatory_model.currentState

        self.assertEqual(obs_current_state.telalt, 86.5)
        self.assertEqual(obs_current_state.telaz, 0.0)
        self.assertEqual(obs_current_state.domalt, 90.0)
        self.assertEqual(obs_current_state.domaz, 0.0)
        self.assertEqual(obs_current_state.filter, 'r')
