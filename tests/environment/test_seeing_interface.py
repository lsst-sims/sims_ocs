import os
import sqlite3
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import SALPY_scheduler

import lsst.utils.tests
from lsst.utils import getPackageDir
from lsst.ts.schedulerConfig import Environment
from lsst.ts.schedulerConfig.instrument import Filters
from lsst.sims.ocs.environment import SeeingInterface
from lsst.sims.utils import TimeHandler

class TestSeeingInterface(unittest.TestCase):
    def setUp(self):
        self.th = TimeHandler("2020-01-01")
        self.seeing = SeeingInterface(self.th)
        self.test_seeing_db = os.path.join(getPackageDir('SIMS_OCS'), 'tests', 'data', 'seeing_test.db')
        self.environment_config = Environment()
        self.environment_config.seeing_db = self.test_seeing_db
        self.filters = Filters()
        # A specific value from the test seeing db to use for testing.
        self.fwhm500_at_900s = 0.851306021213531

    # def cleanUp(self):
    #     tmp = os.listdir(os.path.join(getPackageDir('SIMS_OCS'), 'tests', 'environment'))
    #     osplfiles = []
    #     for t in tmp:
    #         if t.startswith('.ospl'):
    #             osplfiles.append(t)
    #     for t in osplfiles:
    #         os.remove(t)

    # def test_initialize(self):
    #     # Test setup. All variables specified through environment_config.
    #     self.seeing.initialize(self.environment_config, self.filters)
    #     # Note that the seeing DB is specified in environment_config dict.
    #     self.assertEqual(self.seeing.seeingSim.seeing_data.seeing_db, self.environment_config.seeing_db)

    # def test_get_seeing(self):
    #     # Test that retrieving the simple value from seeingdb works.
    #     self.seeing.initialize(self.environment_config, self.filters)
    #     self.assertEqual(self.seeing.get_seeing(900), self.fwhm500_at_900s)
    
    # def test_calculate_seeing(self):
    #     # Test that we can get the FWHM500, FWHMgeom, FWHMeff from calculate_seeing.
    #     # sims_seeingModel tests if this calculation is done correctly. Here we want to check we get 3#'s.
    #     self.seeing.initialize(self.environment_config, self.filters)
    #     fwhm500, fwhmgeom, fwhmeff = self.seeing.calculate_seeing(900, 'g', 1.2)
    #     self.assertEqual(fwhm500, self.fwhm500_at_900s)
    #     self.assertTrue(isinstance(fwhmgeom, float))
    #     self.assertTrue(isinstance(fwhmeff, float))
        
    def test_topic_setting(self):
        seeing_topic = SALPY_scheduler.scheduler_seeingC()
        self.seeing.initialize(self.environment_config, self.filters)
        tstamp = self.th.current_timestamp
        self.th.update_time(40, "minutes")
        self.seeing.set_topic(self.th, seeing_topic)
        self.assertEqual(seeing_topic.timestamp, tstamp + 40 * 60)
        self.assertEqual(seeing_topic.seeing, 0.727564990520477)

"""
class TestSeeingModel(unittest.TestCase):

    def setUp(self):
        self.th = TimeHandler("2020-01-01")
        self.seeing = SeeingInterface(self.th)
        self.environment_config = Environment()
        self.num_original_values = 210384
        self.elapsed_time = 8 * 24 * 3600

    def initialize(self, seeing_dbfile=""):
        self.seeing.initialize(self.environment_config, Filters())

    def compare_seeing(self, seeing_info, truth_fwhm_500_seeing, truth_fwhm_geom_seeing,
                       truth_fwhm_eff_seeing):
        self.assertEqual(seeing_info[0], truth_fwhm_500_seeing)
#        self.assertEqual(seeing_info[1], truth_fwhm_geom_seeing)
        self.assertEqual(seeing_info[2], truth_fwhm_eff_seeing)

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.seeing.seeing_db)
        self.assertIsNone(self.seeing.seeing_dates)
        self.assertIsNone(self.seeing.seeing_values)
        self.assertIsNone(self.seeing.environment_config)
        self.assertIsNone(self.seeing.filters_config)
#        self.assertIsNone(self.seeing.seeing_fwhm_system_zenith)
        self.assertEqual(self.seeing.offset, 0)

    def test_information_after_initialization(self):
        self.initialize()
        self.assertEqual(self.seeing.seeing_values.size, self.num_original_values)
        self.assertEqual(self.seeing.seeing_dates.size, self.num_original_values)
        self.assertIsNotNone(self.seeing.environment_config)

    def test_get_seeing(self):
        self.initialize()
        self.assertEqual(self.seeing.get_seeing(75400), 0.859431982040405)
        self.assertEqual(self.seeing.get_seeing(76700), 0.646009027957916)
        self.assertEqual(self.seeing.get_seeing(63190400), 0.64860999584198)
        self.assertEqual(self.seeing.get_seeing(189424900), 0.699440002441406)

    def test_get_seeing_using_different_start_month(self):
        seeing1 = SeeingInterface(TimeHandler("2020-05-24"))
        seeing1.initialize(self.environment_config, Filters())
        self.assertEqual(seeing1.get_seeing(75400), 0.437314003705978)
        self.assertEqual(seeing1.get_seeing(76700), 0.510206997394562)
        self.assertEqual(seeing1.get_seeing(63190400), 0.453994989395142)
        self.assertEqual(seeing1.get_seeing(189424900), 0.386815994977951)

    def test_alternate_db(self):
        seeing_dbfile = "alternate_seeing.db"

        seeing_table = []
        seeing_table.append("seeingId INTEGER PRIMARY KEY")
        seeing_table.append("s_date INTEGER")
        seeing_table.append("seeing DOUBLE")

        with sqlite3.connect(seeing_dbfile) as conn:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS Seeing")
            cur.execute("CREATE TABLE Seeing({})".format(",".join(seeing_table)))
            cur.executemany("INSERT INTO Seeing VALUES(?, ?, ?)", [(1, 9997, 0.5), (2, 10342, 0.3)])
            cur.close()

        self.environment_config.seeing_db = seeing_dbfile
        self.initialize()
        self.assertEqual(self.seeing.seeing_values.size, 2)
        self.assertEqual(self.seeing.seeing_values[1], 0.3)

        os.remove(seeing_dbfile)

    def test_topic_setting(self):
        seeing_topic = SALPY_scheduler.scheduler_seeingC()
        self.th.update_time(8, "days")
        self.initialize()
        self.seeing.set_topic(self.th, seeing_topic)
        self.assertEqual(seeing_topic.timestamp, 1578528000.0)
        self.assertEqual(seeing_topic.seeing, 0.715884983539581)

    def test_calculation_perfect_seeing_perfect_airmass_in_g_band(self):
        self.initialize()
        self.seeing.get_seeing = mock.MagicMock(return_value=0.0)
        seeing_values = self.seeing.calculate_seeing(self.elapsed_time, 'g', 1.0)
        self.compare_seeing(seeing_values, 0.0, 0.0, 1.16 * 0.39862262855989494)

    def test_calculation_in_g_band(self):
        self.initialize()
        self.seeing.get_seeing = mock.MagicMock(return_value=0.7)
        seeing_values = self.seeing.calculate_seeing(self.elapsed_time, 'g', 1.1)
#        self.compare_seeing(seeing_values, 0.7, 0.74916151132491315, 1.0124922970058186)

    def test_calculation_in_z_band_from_internal_info(self):
        self.initialize()
        seeing_values = self.seeing.calculate_seeing(self.elapsed_time, 'z', 1.5)
#        self.compare_seeing(seeing_values, 0.715884983539581, 0.77351383253748662, 1.0886341618872941)

    def test_bad_filter_name(self):
        self.initialize()
        seeing_values = self.seeing.calculate_seeing(self.elapsed_time, '', 1.5)
        self.compare_seeing(seeing_values, -1.0, -1.0, -1.0)
"""

class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass

def setup_module(module):
    lsst.utils.tests.init()

if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
