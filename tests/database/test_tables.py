import unittest

from sqlalchemy import MetaData

from lsst.sims.ocs.database.tables.base_tbls import create_session

class TablesTest(unittest.TestCase):

    def setUp(self):
        self.metadata = MetaData()

    def test_create_session_table(self):
        session = create_session(self.metadata)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
