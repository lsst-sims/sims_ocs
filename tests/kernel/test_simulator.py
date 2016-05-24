from __future__ import division
from datetime import datetime
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.configuration.sim_config import SimulationConfig
from lsst.sims.ocs.kernel.simulator import Simulator

from tests.database.topic_helpers import exposure_coll1, exposure_coll2, exposure_coll3, exposure_coll4
from tests.database.topic_helpers import slew_activity_coll
from tests.helpers import CONFIG_COMM_PUT_CALLS

class SimulatorTest(unittest.TestCase):

    def setUp(self):
        self.time_tolerance = 1e-6
        self.starting_timestamp = 1640995200.0

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

    def update_timestamp(self, timestamp):
        self.sim.time_handler.current_dt = datetime.utcfromtimestamp(timestamp)

    def check_night_boundary_tuple(self, truth_set_timestamp, truth_rise_timestamp):
        (set_timestamp, rise_timestamp) = self.sim.get_night_boundaries()
        self.assertAlmostEqual(set_timestamp, truth_set_timestamp, delta=self.time_tolerance)
        self.assertAlmostEqual(rise_timestamp, truth_rise_timestamp, delta=self.time_tolerance)

    def test_basic_information_after_creation(self):
        self.assertEqual(self.sim.duration, 183.0)
        self.assertEqual(self.sim.time_handler.initial_timestamp, self.starting_timestamp)
        self.assertIsNotNone(self.sim.obs_site_info)

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
        self.assertEqual(self.mock_salmanager_pub_topic.call_count, 1 + CONFIG_COMM_PUT_CALLS)
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
        # Timestamp, observatory state and observation
        self.put_calls = 3 * self.num_visits
        self.config_comm_put_calls = 1
        self.put_calls += CONFIG_COMM_PUT_CALLS
        self.sim.fractional_duration = 1 / 365
        self.sim.wait_for_scheduler = wait_for_sched
        self.sim.get_night_boundaries = mock.MagicMock(return_value=(self.starting_timestamp,
                                                                     self.starting_timestamp + 360.0))
        self.sim.seq.observatory_model.slew = mock.Mock(return_value=((6.0, "seconds")))
        self.sim.seq.observatory_model.calculate_visit_time = mock.Mock(return_value=((34.0, "seconds")))
        self.sim.seq.observatory_model.target_exposure_list = [exposure_coll1, exposure_coll2]
        self.sim.seq.observatory_model.observation_exposure_list = [exposure_coll3, exposure_coll4]
        self.sim.seq.observatory_model.slew_activities_list = [slew_activity_coll]

        self.assertEqual(self.sim.duration, 1.0)

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
        self.assertEqual(self.mock_socs_db.append_data.call_count, self.num_visits * 11)
        self.assertEqual(self.mock_socs_db.write.call_count, self.num_nights)

    def test_get_night_boundaries(self):
        self.check_night_boundary_tuple(1641084532.843324, 1641113113.755558)
        # 2022/02/01
        self.update_timestamp(1643673600)
        self.check_night_boundary_tuple(1643762299.348505, 1643793352.557206)
        # 2022/03/08
        self.update_timestamp(1646697600)
        self.check_night_boundary_tuple(1646784061.294245, 1646819228.784648)
        # 2022/07/02
        self.update_timestamp(1656720000)
        self.check_night_boundary_tuple(1656802219.515093, 1656845034.696892)
        # 2022/10/17
        self.update_timestamp(1665964800)
        self.check_night_boundary_tuple(1666050479.261601, 1666084046.869362)
        # 2025/04/01
        self.update_timestamp(1743465600)
        self.check_night_boundary_tuple(1743550264.401366, 1743588178.165652)
        # 2027/06/21
        self.update_timestamp(1813536000)
        self.check_night_boundary_tuple(1813618020.702736, 1813660969.989451)
        # 2031/09/20
        self.update_timestamp(1947628800)
        self.check_night_boundary_tuple(1947713387.331446, 1947750106.804758)
