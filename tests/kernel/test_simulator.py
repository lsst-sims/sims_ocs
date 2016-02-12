from __future__ import division
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.configuration.sim_config import SimulationConfig
from lsst.sims.ocs.kernel.simulator import Simulator

from ..helpers import CONFIG_COMM_PUT_CALLS

class SimulatorTest(unittest.TestCase):

    def setUp(self):
        patcher1 = mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.set_publish_topic")
        self.addCleanup(patcher1.stop)
        self.mock_salmanager_pub_topic = patcher1.start()
        patcher2 = mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.set_subscribe_topic")
        self.addCleanup(patcher2.stop)
        self.mock_salmanager_sub_topic = patcher2.start()
        patcher3 = mock.patch("lsst.sims.ocs.database.socs_db.SocsDatabase", spec=True)
        self.addCleanup(patcher3.stop)
        self.mock_socs_db = patcher3.start()

        import collections

        self.options = collections.namedtuple("options", ["frac_duration", "no_scheduler"])
        self.options.frac_duration = 0.5
        self.options.no_scheduler = True

        self.configuration = SimulationConfig()

        self.sim = Simulator(self.options, self.configuration, self.mock_socs_db)

    def test_initial_creation(self):
        self.assertEqual(self.sim.duration, 183.0)
        self.assertEqual(self.sim.time_handler.initial_timestamp, 1640995200.0)
        self.assertEqual(self.sim.seconds_in_night, 10 * 3600)
        self.assertEqual(self.sim.hours_in_daylight, 14)

    def test_fraction_overwrite(self):
        self.sim.fractional_duration = 1 / 365
        self.assertEqual(self.sim.duration, 1.0)

    def test_no_override_from_options(self):
        self.options.frac_duration = -1
        sim = Simulator(self.options, self.configuration, self.mock_socs_db)
        self.assertEquals(sim.duration, 365.0)

    @mock.patch("lsst.sims.ocs.kernel.sequencer.Sequencer.initialize")
    def test_initialization(self, mock_sequencer_init):
        self.sim.initialize()
        self.assertEqual(self.mock_salmanager_pub_topic.call_count, 1)
        self.assertEqual(self.mock_salmanager_sub_topic.call_count, 2)
        self.assertEqual(mock_sequencer_init.call_count, 1)

    @mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.finalize")
    def test_finalization(self, mock_salmanager_final):
        self.sim.finalize()
        self.assertEqual(mock_salmanager_final.call_count, 1)

    def short_run(self, wait_for_sched):
        # Setup for 1 night and 9 visits
        self.num_nights = 1
        self.num_visits = 9
        # One for timestamp and one for observation
        self.put_calls = 2 * self.num_visits
        self.config_comm_put_calls = 1
        self.put_calls += CONFIG_COMM_PUT_CALLS
        self.sim.fractional_duration = 1 / 365
        self.sim.wait_for_scheduler = wait_for_sched
        self.sim.hours_in_night = 0.1
        self.assertEqual(self.sim.duration, 1.0)
        self.assertEqual(self.sim.seconds_in_night, 360)

    @mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.put")
    def test_run_no_scheduler(self, mock_salmanager_put):
        self.short_run(False)

        self.sim.initialize()
        self.sim.run()

        self.assertEqual(mock_salmanager_put.call_count, self.put_calls)
        self.assertEqual(self.sim.seq.targets_received, self.num_visits)
        self.assertEqual(self.sim.seq.observations_made, self.num_visits)

    @mock.patch("SALPY_scheduler.SAL_scheduler")
    @mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.put")
    def test_run_with_scheduler(self, mock_salmanager_put, mock_salscheduler):
        self.short_run(True)
        get_calls = 1 * self.num_visits

        self.sim.initialize()
        # Need to make Scheduler wait break conditions work.
        mock_ss = mock_salscheduler()
        # Fields
        mock_ss.getNextSample_field = mock.MagicMock(return_value=0)
        self.sim.field.ID = -1
        # Targets
        mock_ss.getNextSample_targetTest = mock.MagicMock(return_value=0)
        self.sim.target.num_exposures = 2

        self.sim.run()

        self.assertEqual(mock_salmanager_put.call_count, self.put_calls)
        self.assertEqual(mock_ss.getNextSample_field.call_count, 2)
        self.assertEqual(mock_ss.getNextSample_targetTest.call_count, get_calls)
        self.assertEqual(self.sim.seq.targets_received, self.num_visits)
        self.assertEqual(self.sim.seq.observations_made, self.num_visits)
        self.assertEqual(self.mock_socs_db.clear_data.call_count, self.num_nights)
        self.assertEqual(self.mock_socs_db.append_data.call_count, self.num_visits * 2)
        self.assertEqual(self.mock_socs_db.write.call_count, self.num_nights)
