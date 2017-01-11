import logging
import logging.handlers
try:
    from unittest import mock
except ImportError:
    import mock
import os
import unittest

from lsst.sims.ocs.setup import configure_logging, generate_logfile_path, set_log_levels

class LogTest(unittest.TestCase):

    def setUp(self):
        patcher1 = mock.patch("lsst.sims.ocs.setup.log.get_hostname")
        self.addCleanup(patcher1.stop)
        self.mock_get_hostname = patcher1.start()
        self.hostname = "tester"
        self.mock_get_hostname.return_value = self.hostname

    def test_logfile_creation_path_doesnt_exist(self):
        log_path = generate_logfile_path()
        self.assertEquals(log_path, "{}_1000.log".format(self.hostname))

    def test_logfile_generation_path_exists(self):
        log_dir = "temp_log"
        try:
            os.mkdir(log_dir)
        except OSError:
            os.rmdir(log_dir)
            os.mkdir(log_dir)
        log_path = generate_logfile_path(log_dir)
        self.assertEqual(log_path, os.path.join(log_dir, "{}_1000.log".format(self.hostname)))
        os.rmdir(log_dir)

    def test_verbose_level_zero(self):
        console_detail, file_detail = set_log_levels(0)
        self.assertEqual(console_detail, 0)
        self.assertEqual(file_detail, 3)

    def test_verbose_level_two(self):
        console_detail, file_detail = set_log_levels(2)
        self.assertEqual(console_detail, 2)
        self.assertEqual(file_detail, 3)

    def test_verbose_level_three(self):
        console_detail, file_detail = set_log_levels(2)
        self.assertEqual(console_detail, 2)
        self.assertEqual(file_detail, 3)

    def test_verbose_level_four(self):
        console_detail, file_detail = set_log_levels(4)
        self.assertEqual(console_detail, 2)
        self.assertEqual(file_detail, 4)

    def test_verbose_level_five(self):
        console_detail, file_detail = set_log_levels(6)
        self.assertEqual(console_detail, 2)
        self.assertEqual(file_detail, 5)

    def test_verbose_level_six(self):
        console_detail, file_detail = set_log_levels(6)
        self.assertEqual(console_detail, 2)
        self.assertEqual(file_detail, 5)

    def test_configure_logging(self):
        configure_logging(2, 3)
        self.assertEqual(len(logging.getLogger().handlers), 2)
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.DEBUG)
        handler = logging.getLogger().handlers[-1]
        self.assertIsInstance(handler, logging.handlers.SocketHandler)
        self.assertEqual(handler.port, logging.handlers.DEFAULT_TCP_LOGGING_PORT)

    def test_configure_logging_different_port(self):
        port = 21683
        logging.getLogger().handlers = []
        configure_logging(2, 3, port)
        self.assertEqual(len(logging.getLogger().handlers), 2)
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.DEBUG)
        handler = logging.getLogger().handlers[-1]
        self.assertIsInstance(handler, logging.handlers.SocketHandler)
        self.assertEqual(handler.port, port)
