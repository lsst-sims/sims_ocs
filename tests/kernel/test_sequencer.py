import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.configuration import Observatory, ObservingSite, Survey
from lsst.sims.ocs.kernel.sequencer import Sequencer
from lsst.sims.ocs.kernel.time_handler import TimeHandler
from lsst.sims.ocs.sal.sal_manager import SalManager
from SALPY_scheduler import scheduler_filterSwapC

from tests.helpers import MOON_SUN_INFO, SKY_BRIGHTNESS, TARGET_INFO

class SequencerTest(unittest.TestCase):

    def setUp(self):
        patcher1 = mock.patch("lsst.sims.ocs.kernel.sequencer.AstronomicalSkyModel", spec=True)
        self.addCleanup(patcher1.stop)
        self.mock_astro_sky = patcher1.start()

        self.seq = Sequencer(ObservingSite(), Survey().idle_delay)

    def initialize_sequencer(self):
        self.sal = SalManager()
        self.sal.initialize()
        self.seq.initialize(self.sal, Observatory())

    def create_objects(self):
        target = self.sal.set_subscribe_topic("target")
        # Set some meaningful information
        target.targetId = 10
        target.fieldId = 300
        target.filter = "i"
        target.ra = 0.4244
        target.decl = -0.5314
        target.num_exposures = 2

        # Make it so initial timestamp is 0
        time_handler = TimeHandler("1970-01-01")

        return target, time_handler

    def set_values_for_sky_model(self):
        mas = self.mock_astro_sky.return_value
        mas.date_profile = mock.Mock()
        mas.date_profile.mjd = 59280.1
        mas.get_sky_brightness.return_value = SKY_BRIGHTNESS
        mas.get_target_information.return_value = TARGET_INFO
        mas.get_moon_sun_info.return_value = MOON_SUN_INFO

    def test_basic_information_after_creation(self):
        self.assertEqual(self.seq.observations_made, 0)
        self.assertEqual(self.seq.targets_received, 0)
        self.assertIsNone(self.seq.observation)
        self.assertIsNotNone(self.seq.observatory_model)
        self.assertIsNone(self.seq.observatory_state)
        self.assertIsNotNone(self.seq.observatory_location)
        self.assertEqual(self.seq.targets_missed, 0)
        self.assertIsNotNone(self.seq.sky_model)

    @mock.patch("lsst.sims.ocs.observatory.main_observatory.MainObservatory.configure")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_initialization(self, mock_sal_telemetry_pub, mock_main_observatory_configure):
        self.initialize_sequencer()
        self.assertIsNotNone(self.seq.observation)
        self.assertEqual(self.seq.observation.observationId, 0)
        self.assertEquals(mock_sal_telemetry_pub.call_count, 2)
        self.assertTrue(mock_main_observatory_configure.called)
        self.assertIsNotNone(self.seq.observatory_state)

    @mock.patch("logging.Logger.info")
    def test_finalization(self, mock_logger_info):
        self.seq.finalize()
        self.assertEqual(mock_logger_info.call_count, 3)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_observe_target(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()
        self.set_values_for_sky_model()

        observation, slew, exposures = self.seq.observe_target(target, time_handler)

        self.assertEqual(observation.observation_start_time, time_handler.initial_timestamp + 140.0)
        self.assertEqual(observation.targetId, target.targetId)
        self.assertEqual(observation.sky_brightness, 19.0)
        self.assertEqual(observation.moon_phase, 0.3)
        self.assertEqual(self.seq.targets_received, 1)
        self.assertEqual(self.seq.observations_made, 1)
        self.assertEqual(self.seq.targets_missed, 0)
        self.assertEqual(len(slew), 5)
        self.assertEqual(len(exposures), 2)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_end_night(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()
        self.set_values_for_sky_model()

        # Don't care about outputs
        self.seq.observe_target(target, time_handler)
        self.seq.end_night()

        obs_current_state = self.seq.observatory_model.current_state

        self.assertEqual(obs_current_state.telalt, 86.5)
        self.assertEqual(obs_current_state.telaz, 0.0)
        self.assertEqual(obs_current_state.domalt, 90.0)
        self.assertEqual(obs_current_state.domaz, 0.0)
        self.assertEqual(obs_current_state.filter, target.filter)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_get_observatory_state_after_initialization(self, mock_sal_telemetry_pub,
                                                        mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        _, time_handler = self.create_objects()
        observatory_state = self.seq.get_observatory_state(time_handler.current_timestamp)

        # Observatory state should be in the park position
        self.assertEqual(observatory_state.timestamp, 0.0)
        self.assertEqual(observatory_state.pointing_ra, 29.480264096112467)
        self.assertEqual(observatory_state.pointing_dec, -26.7444)
        self.assertEqual(observatory_state.pointing_altitude, 86.5)
        self.assertEqual(observatory_state.pointing_azimuth, 0.0)
        self.assertEqual(observatory_state.pointing_pa, 180.0)
        self.assertEqual(observatory_state.pointing_rot, 0.0)
        self.assertFalse(observatory_state.tracking)
        self.assertEqual(observatory_state.telescope_altitude, 86.5)
        self.assertEqual(observatory_state.telescope_azimuth, 0.0)
        self.assertEqual(observatory_state.dome_altitude, 90.0)
        self.assertEqual(observatory_state.dome_azimuth, 0.0)
        self.assertEqual(observatory_state.filter_position, 'z')
        self.assertEqual(observatory_state.filter_mounted, 'g,r,i,z,y')
        self.assertEqual(observatory_state.filter_unmounted, 'u')

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    @mock.patch("lsst.sims.ocs.observatory.main_observatory.MainObservatory.start_night")
    def test_start_night(self, mock_obs_son, mock_sal_telemetry_pub, mock_sal_telemetry_sub,
                         mock_logger_log):
        self.initialize_sequencer()
        self.seq.start_night(2281, 3560)
        self.assertTrue(mock_obs_son.called)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_observe_with_no_target(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()
        target.targetId = -1
        target.filter = ''
        target.num_exposures = 1

        observation, slew, exposures = self.seq.observe_target(target, time_handler)

        self.assertEqual(time_handler.current_timestamp, 60.0)
        self.assertEqual(observation.targetId, target.targetId)
        self.assertEqual(observation.filter, 'z')
        self.assertListEqual(list(observation.exposure_times), [15, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(observation.num_exposures, 1)
        self.assertEqual(observation.seeing_fwhm_eff, 0.1)
        self.assertEqual(observation.sky_brightness, 30.0)
        self.assertEqual(observation.airmass, 1.0)
        self.assertEqual(self.seq.targets_received, 0)
        self.assertEqual(self.seq.observations_made, 0)
        self.assertEqual(self.seq.targets_missed, 1)
        self.assertIsNone(slew)
        self.assertIsNone(exposures)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    @mock.patch("lsst.sims.ocs.observatory.main_observatory.MainObservatory.swap_filter")
    def test_start_day(self, mock_obs_sf, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        fs = scheduler_filterSwapC()
        fs.need_swap = True
        fs.filter_to_unmount = 'u'
        self.seq.start_day(fs)
        self.assertTrue(mock_obs_sf.called)
