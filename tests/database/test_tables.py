import unittest

from sqlalchemy import MetaData

import lsst.sims.ocs.database.tables as tbls

import topic_helpers

class TablesTest(unittest.TestCase):

    def setUp(self):
        self.metadata = MetaData()

    def test_create_session_table(self):
        session = tbls.create_session(self.metadata)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
        self.assertTrue(session.c.sessionID.autoincrement)

    def test_create_session_table_without_autoincrement(self):
        session = tbls.create_session(self.metadata, False)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
        self.assertFalse(session.c.sessionID.autoincrement)

    def test_create_target_history_table(self):
        targets = tbls.create_target_history(self.metadata)
        self.assertEqual(len(targets.c), 8)
        self.assertEqual(len(targets.indexes), 3)

    def test_write_target_history_table(self):
        target_topic = topic_helpers.target
        session_id = 1001

        result = tbls.write_target_history(target_topic, session_id)
        self.assertEqual(result['Session_sessionID'], session_id)
        self.assertEqual(result['fieldID'], target_topic.fieldId)
        self.assertEqual(result['filter'], target_topic.filter)
        self.assertEqual(result['dec'], target_topic.dec)

    def test_create_field_table(self):
        fields = tbls.create_field(self.metadata)
        self.assertEqual(len(fields.c), 8)
        self.assertEqual(len(fields.indexes), 4)

    def test_write_field_table(self):
        field_topic = topic_helpers.field_topic

        result = tbls.write_field(field_topic)
        self.assertEqual(result['ID'], field_topic.ID)
        self.assertEqual(result['ra'], field_topic.ra)
        self.assertEqual(result['gb'], field_topic.gb)
        self.assertEqual(result['el'], field_topic.el)

    def test_create_observation_history_table(self):
        obs_hist = tbls.create_observation_history(self.metadata)
        self.assertEqual(len(obs_hist.c), 10)
        self.assertEqual(len(obs_hist.indexes), 4)

    def test_write_observation_history_table(self):
        obs_topic = topic_helpers.observation_topic
        session_id = 1001

        result = tbls.write_observation_history(obs_topic, session_id)
        self.assertEqual(result['Session_sessionID'], session_id)
        self.assertEqual(result['observationID'], obs_topic.observationId)
        self.assertEqual(result['observationTime'], obs_topic.observationTime)
        self.assertEqual(result['targetID'], obs_topic.targetId)
        self.assertEqual(result['fieldID'], obs_topic.fieldId)
        self.assertEqual(result['filter'], obs_topic.filter)
        self.assertEqual(result['dec'], obs_topic.dec)
