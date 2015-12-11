import collections
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
import shutil
import unittest

from lsst.sims.ocs.setup.prog_config import read_file_config, write_file_config

class ProgConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_dir = ".config"
        os.mkdir(cls.config_dir)

        sample_config = """
[Database]
type = mysql

[mysql]
config_path = /home/demouser/mysql
        """
        cls.config_file = "opsim4_testing"
        with open(os.path.join(cls.config_dir, cls.config_file), 'w') as cfile:
            cfile.write(sample_config)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.config_dir)

    def setUp(self):
        self.options = collections.namedtuple("options", ["type", "save_dir"])
        self.options.type = "sqlite"
        self.options.save_dir = "/home/demouser/run/output"

    def test_write_file(self):
        write_file_config(self.options, self.config_dir)
        file_path = os.path.join(self.config_dir, "opsim4")
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))

    def test_read_file(self):
        parser = read_file_config(self.config_file, self.config_dir)
        self.assertEqual(parser.get("Database", "type"), "mysql")
        self.assertEqual(parser.get("mysql", "config_path"), "/home/demouser/mysql")

    def test_read_no_file(self):
        parser = read_file_config("opsim3", self.config_dir)
        self.assertIsNone(parser)

    def test_read_file_no_section(self):
        parser = read_file_config(self.config_file, self.config_dir)
        with self.assertRaises(configparser.NoSectionError):
            parser.get("sqlite", "save_directory")

    def test_read_file_section_no_option(self):
        parser = read_file_config(self.config_file, self.config_dir)
        with self.assertRaises(configparser.NoOptionError):
            parser.get("mysql", "save_directory")
