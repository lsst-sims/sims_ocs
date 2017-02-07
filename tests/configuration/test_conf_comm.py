import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.configuration.conf_comm import ConfigurationCommunicator
from lsst.sims.ocs.configuration.sim_config import SimulationConfig
from lsst.sims.ocs.sal.sal_manager import SalManager

from tests.helpers import CONFIG_COMM_PUB_CALLS, CONFIG_COMM_PUT_CALLS
from tests.helpers import NUM_GEN_PROPS, NUM_SEQ_PROPS

class ConfigurationCommunicatorTest(unittest.TestCase):

    def setUp(self):
        self.conf_comm = ConfigurationCommunicator()
        self.sal = SalManager()
        self.sal.initialize()
        self.config = SimulationConfig()
        self.config.load_proposals()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.conf_comm.sal)
        self.assertIsNone(self.conf_comm.config)

    def test_initialize(self):
        self.conf_comm.initialize(self.sal, self.config)
        self.assertIsNotNone(self.conf_comm.sal)
        self.assertIsNotNone(self.conf_comm.config)

    @mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.put")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_run(self, mock_sal_telemetry_pub, mock_salmanager_put):
        self.conf_comm.initialize(self.sal, self.config)
        self.conf_comm.run()
        self.assertEqual(mock_sal_telemetry_pub.call_count, CONFIG_COMM_PUB_CALLS)
        # FIXME: Extra -1 needed while sequence proposal sending commented out.
        self.assertEqual(mock_salmanager_put.call_count,
                         CONFIG_COMM_PUT_CALLS + NUM_GEN_PROPS + NUM_SEQ_PROPS - 1)
