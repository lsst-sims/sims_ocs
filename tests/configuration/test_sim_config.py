import os
import shutil
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.configuration import SimulationConfig
from tests.helpers import CONFIG_COMM_PUT_CALLS, NUM_AREA_DIST_PROPS

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

def create_content(mod_name, cclass, cvars):
    return """import {}
assert type(config)=={}.{}, 'config is of type %s.%s instead of {}.{}' % (type(config).__module__,
 type(config).__name__)
{}
                  """.format(mod_name, mod_name, cclass, mod_name, cclass, os.linesep.join(cvars))

class SimulationConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file1 = create_file(1)
        cls.file2 = create_file(2)
        cls.file3 = create_file(3)
        cls.config_dir = "config_temp"
        os.mkdir(cls.config_dir)
        cls.file4 = create_file(4, cls.config_dir)
        cls.file5 = create_file(5, message=create_content("lsst.sims.ocs.configuration.survey",
                                                          "Survey", ["config.duration=10.0"]))
        cls.file6 = create_file(6,
                                message=create_content(
                                    "lsst.sims.ocs.configuration.instrument.optics_loop_corr",
                                    "OpticsLoopCorr", ["config.tel_optics_cl_delay=[0.0, 18.0]"]))

        cls.config_save_dir = "config_save"
        os.mkdir(cls.config_save_dir)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.file1)
        os.remove(cls.file2)
        os.remove(cls.file3)
        shutil.rmtree(cls.config_dir)
        os.remove(cls.file5)
        os.remove(cls.file6)
        shutil.rmtree(cls.config_save_dir)

    def setUp(self):
        self.sim_config = SimulationConfig()

    def test_basic_information_from_creation(self):
        self.assertIsNotNone(self.sim_config.survey)
        self.assertIsNotNone(self.sim_config.science)
        self.assertIsNotNone(self.sim_config.observing_site)
        self.assertIsNotNone(self.sim_config.observatory)
        self.assertIsNotNone(self.sim_config.downtime)
        self.assertIsNotNone(self.sim_config.sched_driver)

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
        self.assertEqual(self.sim_config.survey.duration, 10.0)
        self.sim_config.load([self.file6])
        self.assertEqual(self.sim_config.observatory.optics_loop_corr.tel_optics_cl_delay[1], 18.0)

    @mock.patch("lsst.pex.config.Config.save")
    def test_saving_blank_configurations(self, mock_pexconfig_save):
        # The real configurations can get very expensive to save, so we're just testing that the
        # correct number of executions and blank files are created. The extra 2 is due
        # to the downtime and environment config not needing to be sent via conf_comm.
        self.sim_config.load_proposals()
        self.assertEqual(len(self.sim_config.science.area_dist_props.active), NUM_AREA_DIST_PROPS)
        expected_calls = CONFIG_COMM_PUT_CALLS + NUM_AREA_DIST_PROPS + 2
        save_files = ["save_conf{}.py".format(i + 1) for i in range(expected_calls)]
        mock_pexconfig_save.side_effect = [save_file(f, self.config_save_dir) for f in save_files]
        self.sim_config.save(self.config_save_dir)
        self.assertEqual(mock_pexconfig_save.call_count, expected_calls)
        self.assertEqual(len(os.listdir(self.config_save_dir)), expected_calls)

    def test_load_proposals(self):
        with self.assertRaises(TypeError):
            self.assertEqual(len(self.sim_config.science.area_dist_props.names), NUM_AREA_DIST_PROPS)

        self.sim_config.load_proposals()
        self.assertEqual(self.sim_config.num_proposals, NUM_AREA_DIST_PROPS)
        self.assertEqual(len(self.sim_config.science.area_dist_props.names), NUM_AREA_DIST_PROPS)
        self.assertEqual(len(self.sim_config.science.area_dist_props.active), NUM_AREA_DIST_PROPS)

    def test_load_specifc_proposals(self):
        self.sim_config.survey.ad_proposals = ["GalacticPlane", "SouthCelestialPole"]
        self.sim_config.load_proposals()
        self.assertEqual(len(self.sim_config.science.area_dist_props.names), 2)
        self.assertEqual(len(self.sim_config.science.area_dist_props.active), 2)

    def test_load_no_proposals(self):
        self.sim_config.survey.ad_proposals = []
        self.sim_config.load_proposals()
        self.assertEqual(self.sim_config.num_proposals, 0)
        with self.assertRaises(TypeError):
            self.assertEqual(len(self.sim_config.science.area_dist_props.names), 0)
        with self.assertRaises(TypeError):
            self.assertEqual(len(self.sim_config.science.area_dist_props.active), 0)
