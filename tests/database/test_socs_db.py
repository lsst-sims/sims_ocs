import os
import random
import shutil
from sqlalchemy import create_engine, select
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.database.socs_db import SocsDatabase
from lsst.sims.ocs.database.tables import write_target_history
import topic_helpers

class SocsDatabaseSqliteTest(unittest.TestCase):

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def setUp(self, mock_get_hostname):
        self.hostname = "tester{:02d}".format(random.randrange(0, 19))
        self.db_name = "{}_sessions.db".format(self.hostname)
        mock_get_hostname.return_value = self.hostname

        self.db = SocsDatabase()
        self.session_id = -1

    def tearDown(self):
        session_db_name = "{}_{}.db".format(self.hostname, self.session_id)
        if os.path.exists(session_db_name):
            os.remove(session_db_name)
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def setup_db(self, startup_comment, mock_get_hostname):
        mock_get_hostname.return_value = self.hostname
        self.db.create_db()
        self.session_id = self.db.new_session(startup_comment)

    def create_append_data(self):
        target = topic_helpers.target
        self.db.append_data("target_history", target)

    def check_db_file_for_target_info(self):
        session_db_name = "{}_{}.db".format(self.hostname, self.session_id)
        engine = create_engine("sqlite:///{}".format(session_db_name))
        conn = engine.connect()
        th = getattr(self.db, "target_history")
        s = select([th])
        result = conn.execute(s)
        row = result.fetchone()
        self.assertEqual(len(row), len(th.c))
        target = topic_helpers.target
        self.assertEqual(row['Field_fieldId'], target.fieldId)

    def test_basic_information_after_creation(self):
        self.assertEqual(self.db.db_dialect, "sqlite")
        self.assertIsNotNone(self.db.engine)
        self.assertIsNotNone(self.db.metadata)
        self.assertTrue(hasattr(self.db, "session_tracking"))

    def test_database_creation(self):
        self.db.create_db()
        self.assertTrue(os.path.exists(self.db_name))

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def test_new_session(self, mock_get_hostname):
        mock_get_hostname.return_value = self.hostname
        session_id_truth = 2000
        startup_comment = "This is my cool test!"

        self.db.create_db()
        session_id = self.db.new_session(startup_comment)

        self.assertEqual(session_id, session_id_truth)
        session_db_name = "{}_{}.db".format(self.hostname, session_id_truth)
        self.assertTrue(os.path.exists(session_db_name))
        if os.path.exists(session_db_name):
            os.remove(session_db_name)

    def test_append_data(self):
        self.setup_db("This is my cool test!")
        self.create_append_data()
        self.assertEqual(len(self.db.data_list), 1)
        self.assertEqual(len(self.db.data_list["target_history"]), 1)

    def test_append_data_after_clear(self):
        self.setup_db("This is my cool test!")
        self.create_append_data()
        self.db.clear_data()
        self.create_append_data()
        self.assertEqual(len(self.db.data_list), 1)
        self.assertEqual(len(self.db.data_list["target_history"]), 1)

    def test_clear_data(self):
        self.setup_db("This is my cool test!")
        self.create_append_data()
        self.db.clear_data()
        self.assertEqual(len(self.db.data_list), 0)

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def test_write_data(self, mock_get_hostname):
        mock_get_hostname.return_value = self.hostname
        self.setup_db("This is my cool test!")
        self.create_append_data()

        self.db.write()
        self.check_db_file_for_target_info()

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def test_write_table_data(self, mock_get_hostname):
        mock_get_hostname.return_value = self.hostname
        self.setup_db("This is my cool test!")

        target = topic_helpers.target
        self.db.write_table("target_history", [write_target_history(target, self.session_id)])
        self.check_db_file_for_target_info()

class SocsDatabaseSqliteWithSavePathTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.save_path = "output"
        os.mkdir(cls.save_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.save_path)

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def setUp(self, mock_get_hostname):
        self.hostname = "tester"
        self.db_name = "{}_sessions.db".format(self.hostname)
        mock_get_hostname.return_value = self.hostname
        self.db = SocsDatabase(sqlite_save_path=self.save_path)

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.db.sqlite_save_path)
        self.assertEqual(self.db.sqlite_save_path, self.save_path)

    def test_database_creation(self):
        self.db.create_db()
        self.assertTrue(os.path.exists(os.path.join(self.save_path, self.db_name)))
