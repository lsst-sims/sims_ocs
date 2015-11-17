import os
import random
import shutil
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.database.socs_db import SocsDatabase

class SocsDatabaseMySqlTest(unittest.TestCase):

    def setUp(self):
        self.db = SocsDatabase()

    def test_initial_creation(self):
        self.assertEqual(self.db.db_dialect, "mysql")
        self.assertIsNotNone(self.db.engine)
        self.assertIsNotNone(self.db.metadata)
        self.assertTrue(hasattr(self.db, "session"))

    @mock.patch("sqlalchemy.MetaData.create_all")
    def test_database_creation(self, mock_create_all):
        self.db.create_db()
        self.assertIsNotNone(self.db.engine)
        mock_create_all.called_once_with(self.db.engine)

    @mock.patch("sqlalchemy.MetaData.drop_all")
    def test_database_deletion(self, mock_drop_all):
        self.db.delete_db()
        self.assertIsNotNone(self.db.engine)
        mock_drop_all.called_once_with(self.db.engine)

    @mock.patch("sqlalchemy.engine.Connection", autospec=True)
    @mock.patch("sqlalchemy.engine.Engine", autospec=True)
    @mock.patch("lsst.sims.ocs.database.socs_db.create_engine")
    def test_new_session(self, mock_create_engine, mock_engine, mock_conn):
        # Need all the mocks to avoid writing to a real DB.
        session_id_truth = 1000
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value = mock_conn
        mock_result = mock.Mock()
        mock_result.lastrowid = session_id_truth
        mock_conn.execute.return_value = mock_result

        # Need a fresh DB object with this one!
        db = SocsDatabase()
        startup_comment = "This is my cool test!"
        session_id = db.new_session(startup_comment)

        self.assertEqual(mock_conn.execute.call_count, 1)
        self.assertEqual(session_id, session_id_truth)

class SocsDatabaseSqliteTest(unittest.TestCase):

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def setUp(self, mock_get_hostname):
        self.hostname = "tester{:02d}".format(random.randrange(0, 19))
        self.db_name = "{}_sessions.db".format(self.hostname)
        mock_get_hostname.return_value = self.hostname

        self.db = SocsDatabase("sqlite")

    def tearDown(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_initial_creation(self):
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
        session_id_truth = 1000
        startup_comment = "This is my cool test!"

        self.db.create_db()
        session_id = self.db.new_session(startup_comment)

        self.assertEqual(session_id, session_id_truth)
        session_db_name = "{}_{}.db".format(self.hostname, session_id_truth)
        self.assertTrue(os.path.exists(session_db_name))
        if os.path.exists(session_db_name):
            os.remove(session_db_name)

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

        self.db = SocsDatabase("sqlite", sqlite_save_path=self.save_path)

    def test_initial_creation(self):
        self.assertIsNotNone(self.db.sqlite_save_path)
        self.assertEqual(self.db.sqlite_save_path, self.save_path)

    def test_database_creation(self):
        self.db.create_db()
        self.assertTrue(os.path.exists(os.path.join(self.save_path, self.db_name)))
