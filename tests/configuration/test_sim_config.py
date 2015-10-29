import os
import shutil
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.configuration.sim_config import SimulationConfig

def create_file(i, directory=None, message=None):
    filename = "conf{}.py".format(i)
    if directory is not None:
        filename = os.path.join(directory, filename)
    ifile = open(filename, 'w')
    if message is not None:
        ifile.write(message)
    ifile.close()
    return filename

def save_file(filename, save_dir):
    ifile = open(os.path.join(save_dir, filename), 'w')
    ifile.close()

class SimulationConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file1 = create_file(1)
        cls.file2 = create_file(2)
        cls.file3 = create_file(3)
        cls.config_dir = "config_temp"
        os.mkdir(cls.config_dir)
        cls.file4 = create_file(4, cls.config_dir)

        module = "lsst.sims.ocs.configuration.lsst_survey"
        conf_class = "LsstSurvey"
        content = """import {}
assert type(config)=={}.{}, 'config is of type %s.%s instead of {}.{}' % (type(config).__module__,
 type(config).__name__)
config.duration=10.0
                  """.format(module, module, conf_class, module, conf_class)
        cls.file5 = create_file(5, message=content)

        cls.config_save_dir = "config_save"
        os.mkdir(cls.config_save_dir)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.file1)
        os.remove(cls.file2)
        os.remove(cls.file3)
        shutil.rmtree(cls.config_dir)
        os.remove(cls.file5)
        shutil.rmtree(cls.config_save_dir)

    def setUp(self):
        self.sim_config = SimulationConfig()

    def test_basic_information_from_creation(self):
        self.assertIsNotNone(self.sim_config.lsst_survey)
        self.assertIsNotNone(self.sim_config.observing_site)

    def test_load_without_files(self):
        self.sim_config.load(None)

    def test_load_from_single_file(self):
        self.sim_config.load([self.file1])

    def test_load_from_multiple_files(self):
        self.sim_config.load([self.file1, self.file2, self.file3])

    def test_load_from_directory(self):
        self.sim_config.load([self.config_dir])

    def test_load_does_override(self):
        self.sim_config.load([self.file5])
        self.assertEqual(self.sim_config.lsst_survey.duration, 10.0)

    @mock.patch("lsst.pex.config.Config.save")
    def test_saving_blank_configurations(self, mock_pexconfig_save):
        # The real configurations can get very expensive to save, so we're just testing that the
        # correct number of executions and blank files are created.
        expected_calls = 2
        save_files = ["save_conf{}.py".format(i + 1) for i in range(expected_calls)]
        mock_pexconfig_save.side_effect = [save_file(f, self.config_save_dir) for f in save_files]
        self.sim_config.save(self.config_save_dir)
        self.assertEqual(mock_pexconfig_save.call_count, expected_calls)
        self.assertEqual(len(os.listdir(self.config_save_dir)), expected_calls)
