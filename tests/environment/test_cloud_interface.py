import os
import sqlite3
import unittest

import SALPY_scheduler

from lsst.utils import getPackageDir
import lsst.utils.tests
from lsst.sims.ocs.environment import CloudInterface
from lsst.sims.utils import TimeHandler


class TestCloudInterface(unittest.TestCase):
    def setUp(self):
        self.th = TimeHandler("2020-01-01")
        self.cloud = CloudInterface(self.th)
        # Self-contained test database.
        self.test_db = os.path.join(getPackageDir('SIMS_OCS'), 'tests', 'data', 'cloud_test.db')

    # def cleanUp(self):
    #     tmp = os.listdir(os.path.join(getPackageDir('SIMS_OCS'), 'tests', 'environment'))
    #     osplfiles = []
    #     for t in tmp:
    #         if t.startswith('.ospl'):
    #             osplfiles.append(t)
    #     for t in osplfiles:
    #         os.remove(t)

    # def test_initialization(self):
    #     # Test initialization with default information.
    #     self.cloud.initialize()
    #     default_db = os.path.join(getPackageDir('SIMS_CLOUDMODEL'), 'data', 'cloud.db')
    #     self.assertEqual(self.cloud.cloud_model.cloud_db, default_db)
    #     self.assertTrue(len(self.cloud.cloud_model.cloud_dates) > 0)
    #     # Test initialization with custom information.
    #     self.cloud.initialize(self.test_db)
    #     self.assertEqual(self.cloud.cloud_model.cloud_db, self.test_db)
    #     self.assertTrue(len(self.cloud.cloud_model.cloud_dates), 10)
    
    # def test_get_cloud(self):
    #     # Can't be sure of order of tests. 
    #     # Reread database, but use testdb to be sure we're getting the info we expect.
    #     self.cloud.initialize(self.test_db)
    #     self.assertEqual(self.cloud.get_cloud(96300), 0.0)
    #     self.assertEqual(self.cloud.get_cloud(110781), 0.0)

    def test_topic_setting(self):
        timeHandler = TimeHandler("2020-01-01")
        tstamp = timeHandler.current_timestamp
        cloud = CloudInterface(timeHandler)
        cloud.initialize(self.test_db)
        cloud_topic = SALPY_scheduler.scheduler_bulkCloudC()
        timeHandler.update_time(6, "hours")
        cloud.set_topic(timeHandler, cloud_topic)
        tstamp = tstamp + 6 * 60.0 * 60.0
        self.assertEqual(cloud_topic.timestamp, tstamp)
        self.assertEqual(cloud_topic.bulk_cloud, 0.0)

"""
class TestCloudModel(unittest.TestCase):

    def setUp(self):
        self.th = TimeHandler("2020-01-01")
        self.cloud = CloudInterface(self.th)
        self.cloud_model = self.cloud.cloud_model
        self.num_original_values = 29201

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.cloud_model.cloud_db)
        self.assertIsNone(self.cloud_model.cloud_dates)
        self.assertIsNone(self.cloud_model.cloud_values)
        self.assertEqual(self.cloud_model.offset, 0)

    def test_information_after_initialization(self):
        self.cloud.initialize()
        self.assertEqual(self.cloud_model.cloud_values.size, self.num_original_values)
        self.assertEqual(self.cloud_model.cloud_dates.size, self.num_original_values)

    def test_get_clouds(self):
        self.cloud.initialize()
        self.assertEqual(self.cloud_model.get_cloud(700000), 0.5)
        self.assertEqual(self.cloud_model.get_cloud(701500), 0.5)
        self.assertEqual(self.cloud_model.get_cloud(705000), 0.375)
        self.assertEqual(self.cloud_model.get_cloud(630684000), 0.0)

    def test_get_clouds_using_different_start_month(self):
        cloud1 = CloudInterface(TimeHandler("2020-05-24"))
        cloud_model1 = cloud1_model
        self.assertEqual(cloud1_model.offset, 12441600)
        cloud1.initialize()
        self.assertEqual(cloud1_model.get_cloud(700000), 0.0)
        self.assertEqual(cloud1_model.get_cloud(701500), 0.0)
        self.assertEqual(cloud1_model.get_cloud(705000), 0.0)
        self.assertEqual(cloud1_model.get_cloud(630684000), 0.25)

    def test_alternate_db(self):
        cloud_dbfile = "alternate_cloud.db"

        cloud_table = []
        cloud_table.append("cloudId INTEGER PRIMARY KEY")
        cloud_table.append("c_date INTEGER")
        cloud_table.append("cloud DOUBLE")

        with sqlite3.connect(cloud_dbfile) as conn:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS Cloud")
            cur.execute("CREATE TABLE Cloud({})".format(",".join(cloud_table)))
            cur.executemany("INSERT INTO Cloud VALUES(?, ?, ?)", [(1, 9997, 0.5), (2, 10342, 0.125)])
            cur.close()

        self.cloud.initialize(cloud_dbfile)
        self.assertEqual(self.cloud.cloud_values.size, 2)
        self.assertEqual(self.cloud.cloud_values[1], 0.125)

        os.remove(cloud_dbfile)

    def test_topic_setting(self):
        cloud_topic = SALPY_scheduler.scheduler_cloudC()
        self.th.update_time(8, "days")
        self.cloud.initialize()
        self.cloud.set_topic(self.th, cloud_topic)
        self.assertEqual(cloud_topic.timestamp, 1578528000.0)
        self.assertEqual(cloud_topic.cloud, 0.5)
"""

class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass

def setup_module(module):
    lsst.utils.tests.init()

if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
