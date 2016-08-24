import os
import sqlite3
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.environment import SeeingModel

class TestSeeingModel(unittest.TestCase):

    def setUp(self):
        self.seeing = SeeingModel()
        self.num_original_values = 210384

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.seeing.seeing_db)
        self.assertIsNone(self.seeing.seeing_dates)
        self.assertIsNone(self.seeing.seeing_values)

    def test_information_after_initialization(self):
        self.seeing.initialize()
        self.assertEqual(self.seeing.seeing_values.size, self.num_original_values)
        self.assertEqual(self.seeing.seeing_dates.size, self.num_original_values)

    def test_get_seeing(self):
        self.seeing.initialize()
        self.assertEqual(self.seeing.get_seeing(75400), 0.859431982040405)
        self.assertEqual(self.seeing.get_seeing(76700), 0.646009027957916)
        self.assertEqual(self.seeing.get_seeing(63190400), 0.64860999584198)
        self.assertEqual(self.seeing.get_seeing(189424900), 0.699440002441406)

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

        self.seeing.initialize(seeing_dbfile)
        self.assertEqual(self.seeing.seeing_values.size, 2)
        self.assertEqual(self.seeing.seeing_values[1], 0.3)

        os.remove(seeing_dbfile)

    @mock.patch("lsst.sims.ocs.database.socs_db.SocsDatabase", spec=True)
    def test_database_write(self, mock_db):
        self.seeing.initialize()
        self.seeing.write_to_db(mock_db)
        self.assertEqual(mock_db.write_table.call_count, 1)
