import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.kernel.simulator import Simulator

class SimulatorTest(unittest.TestCase):

    def setUp(self):
        self.sim = Simulator(0.5)

    def test_initial_creation(self):
        self.assertEqual(self.sim.duration, 183.0)
        self.assertEqual(self.sim.time_handler.initial_timestamp, 1590278400.0)

    def test_fraction_overwrite(self):
        self.sim.fractional_duration = 1.0 / 365.0
        self.assertEqual(self.sim.duration, 1.0)

    @mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.set_subscribe_topic")
    @mock.patch("lsst.sims.ocs.sal.sal_manager.SalManager.set_publish_topic")
    def test_initialization(self, mock_salmanager_pub_topic, mock_salmanager_sub_topic):
        self.sim.initialize()
        self.assertEqual(mock_salmanager_pub_topic.call_count, 2)
        self.assertEqual(mock_salmanager_sub_topic.call_count, 1)
