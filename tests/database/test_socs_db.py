import os
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
        self.assertIsNone(self.db.engine)
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

class SocsDatabaseSqliteTest(unittest.TestCase):

    def setUp(self):
        self.db = SocsDatabase("sqlite")
        self.hostname = "tester"
        self.db_name = "{}_sessions.db".format(self.hostname)

    def tearDown(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_initial_creation(self):
        self.assertEqual(self.db.db_dialect, "sqlite")
        self.assertIsNone(self.db.engine)
        self.assertIsNotNone(self.db.metadata)
        self.assertTrue(hasattr(self.db, "session_tracking"))

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def test_database_creation(self, mock_get_hostname):
        mock_get_hostname.return_value = self.hostname
        self.db.create_db()
        self.assertTrue(os.path.exists(self.db_name))

class SocsDatabaseSqliteWithSavePathTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.save_path = "output"
        os.mkdir(cls.save_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.save_path)

    def setUp(self):
        self.db = SocsDatabase("sqlite", sqlite_save_path=self.save_path)
        self.hostname = "tester"
        self.db_name = "{}_sessions.db".format(self.hostname)

    def test_initial_creation(self):
        self.assertIsNotNone(self.db.sqlite_save_path)
        self.assertEqual(self.db.sqlite_save_path, self.save_path)

    @mock.patch("lsst.sims.ocs.database.socs_db.get_hostname")
    def test_database_creation(self, mock_get_hostname):
        mock_get_hostname.return_value = self.hostname
        self.db.create_db()
        self.assertTrue(os.path.exists(os.path.join(self.save_path, self.db_name)))
