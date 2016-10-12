import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.sal.sal_manager import SalManager
from SALPY_scheduler import scheduler_targetC

class SalManagerTest(unittest.TestCase):

    def setUp(self):
        self.sal = SalManager()
        self.sal_debug_level = 0
        # If below is changed, make sure to update patch call on test_publishing_topic
        self.publish_topic = "timeHandler"

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.sal)
        self.assertEquals(self.sal.debug_level, self.sal_debug_level)
        self.assertIsNone(self.sal.manager)

    def test_after_initialization(self):
        self.sal.initialize()
        self.assertIsNotNone(self.sal.manager)
        self.assertEquals(self.sal.manager.getDebugLevel(-1), self.sal_debug_level)

    @mock.patch("SALPY_scheduler.SAL_scheduler.salShutdown")
    def test_finalize(self, mock_sal_shutdown):
        self.sal.initialize()
        self.sal.finalize()
        self.assertTrue(mock_sal_shutdown.called)

    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_setting_publish_topic(self, mock_sal_telemetry_pub):
        self.sal.initialize()
        topic_name = self.publish_topic
        topic = self.sal.set_publish_topic(topic_name)
        self.assertIsNotNone(topic)
        self.assertEqual(topic.timestamp, 0)
        self.assertTrue(mock_sal_telemetry_pub.called)

    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    def test_setting_subscribe_topic(self, mock_sal_telemetry_sub):
        self.sal.initialize()
        topic_name = "target"
        topic = self.sal.set_subscribe_topic(topic_name)
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, scheduler_targetC)
        self.assertEqual(topic.targetId, 0)
        self.assertTrue(mock_sal_telemetry_sub.called)

    @mock.patch("SALPY_scheduler.SAL_scheduler.putSample_timeHandler")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_publishing_topic(self, mock_sal_telemetry_sub, mock_sal_put_sample):
        self.sal.initialize()
        topic = self.sal.set_publish_topic(self.publish_topic)
        self.sal.put(topic)
        self.assertTrue(mock_sal_put_sample.called)

    def test_get_topic(self):
        self.sal.initialize()
        topic = self.sal.get_topic(self.publish_topic)
        self.assertIsNotNone(topic)
