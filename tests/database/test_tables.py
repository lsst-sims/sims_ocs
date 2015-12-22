import unittest

from sqlalchemy import MetaData

from lsst.sims.ocs.database.tables.base_tbls import create_session, create_target_history
from lsst.sims.ocs.database.tables.write_tbls import write_target_history

import topic_helpers

class TablesTest(unittest.TestCase):

    def setUp(self):
        self.metadata = MetaData()

    def test_create_session_table(self):
        session = create_session(self.metadata)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
        self.assertTrue(session.c.sessionID.autoincrement)

    def test_create_session_table_without_autoincrement(self):
        session = create_session(self.metadata, False)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
        self.assertFalse(session.c.sessionID.autoincrement)

    def test_create_target_history_table(self):
        targets = create_target_history(self.metadata)
        self.assertEqual(len(targets.c), 8)
        self.assertEqual(len(targets.indexes), 3)

    def test_write_target_history_table(self):
        target_topic = topic_helpers.target
        session_id = 1001

        result = write_target_history(target_topic, session_id)
        self.assertEqual(result['Session_sessionID'], session_id)
        self.assertEqual(result['fieldID'], target_topic.fieldId)
        self.assertEqual(result['filter'], target_topic.filter)
        self.assertEqual(result['dec'], target_topic.dec)
