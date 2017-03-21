import collections
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    from unittest import mock
except ImportError:
    import mock
import os
import shutil
import unittest

from lsst.sims.ocs.setup.prog_config import apply_file_config, read_file_config, write_file_config

class ProgConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_dir = ".config"
        os.mkdir(cls.config_dir)

        sample_config = """
[Database]
type = sqlite

[sqlite]
save_directory = /home/demouser/run/output
        """
        cls.config_file = "opsim4_testing"
        with open(os.path.join(cls.config_dir, cls.config_file), 'w') as cfile:
            cfile.write(sample_config)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.config_dir)

    def setUp(self):
        self.options = collections.namedtuple("options", ["type", "save_dir", "session_save_dir"])

    def sqlite_options(self):
        self.options.type = "sqlite"
        self.options.save_dir = "/home/demouser/run/output"
        self.options.session_save_dir = None
        self.options.session_id_start = "1040"

    def check_written_file(self):
        file_path = os.path.join(self.config_dir, "opsim4")
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))

    def test_write_sqlite_file(self):
        self.sqlite_options()
        write_file_config(self.options, self.config_dir)
        self.check_written_file()

    def test_write_file_no_config_dir(self):
        with mock.patch.dict('os.environ', {"HOME": '.'}, clear=True):
            self.sqlite_options()
            write_file_config(self.options)
            self.check_written_file()

    def test_read_file(self):
        parser = read_file_config(self.config_file, self.config_dir)
        self.assertEqual(parser.get("Database", "type"), "sqlite")
        self.assertEqual(parser.get("sqlite", "save_directory"), "/home/demouser/run/output")

    def test_read_no_file(self):
        parser = read_file_config("opsim3", self.config_dir)
        self.assertIsNone(parser)

    def test_read_default_file(self):
        parser = read_file_config(None, self.config_dir)
        self.assertIsNone(parser)

    def test_read_file_no_config_dir(self):
        with mock.patch.dict('os.environ', {"HOME": '.'}, clear=True):
            parser = read_file_config(self.config_file)
            self.assertEqual(parser.get("Database", "type"), "sqlite")

    def test_read_file_no_section(self):
        parser = read_file_config(self.config_file, self.config_dir)
        with self.assertRaises(configparser.NoSectionError):
            parser.get("mysql", "save_directory")

    def test_read_file_section_no_option(self):
        parser = read_file_config(self.config_file, self.config_dir)
        with self.assertRaises(configparser.NoOptionError):
            parser.get("sqlite", "config_path")

    def test_option_override_with_sqlite_as_db(self):
        sample_config = """
[Database]
type = sqlite

[sqlite]
save_directory = /home/demouser/storage
session_save_directory = /home/demouser/output
session_id_start = 2345

[track_session]
track = True
tracking_db = http://fun.new.machine.edu/tracking
        """
        config_file = "opsim4_options_with_sqlite_testing"
        with open(os.path.join('.', config_file), 'w') as cfile:
            cfile.write(sample_config)

        config = read_file_config(config_file, '.')

        options = collections.namedtuple("options", ["db_type", "sqlite_save_dir",
                                                     "sqlite_session_save_dir", "session_id_start",
                                                     "track_session", "tracking_db"])
        # Set option defaults
        options.db_type = "mysql"
        options.sqlite_save_dir = None
        options.sqlite_session_save_dir = None
        options.session_id_start = None
        options.track_session = False
        options.tracking_db = None

        apply_file_config(config, options)
        self.assertEqual(options.db_type, "sqlite")
        self.assertEqual(options.sqlite_save_dir, "/home/demouser/storage")
        self.assertEqual(options.sqlite_session_save_dir, "/home/demouser/output")
        self.assertEqual(options.session_id_start, 2345)
        self.assertTrue(options.track_session)
        self.assertEqual(options.tracking_db, "http://fun.new.machine.edu/tracking")

        os.remove(config_file)
