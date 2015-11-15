import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.database.socs_db import SocsDatabase

class SocsDatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = SocsDatabase()

    def test_initial_creation(self):
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
