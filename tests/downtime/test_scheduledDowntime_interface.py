import logging
import os
import sqlite3
import unittest

from lsst.sims.ocs.downtime.scheduledDowntime_interface import ScheduledDowntimeInterface

class ScheduledDowntimeTest(unittest.TestCase):

    def setUp(self):
        self.sdt = ScheduledDowntimeInterface()
        logging.getLogger().setLevel(logging.WARN)
    
    # Tests commented out for now since these already reside within the standalone package. The only testing that SOCS
    # should be doing with these packages are topic related. Otherwise in order to test the package properly getters 
    # need to be in place, however having this is not very sensible since the only reason the method exists for is for
    # testing. All tests (except SALPY related ones) to be removed once the tasks have been made for it.

    # def check_downtime(self, downtime, night, duration, activity):
    #     self.assertEqual(downtime[0], night)
    #     self.assertEqual(downtime[1], duration)
    #     self.assertEqual(downtime[2], activity)

    # def test_basic_information_after_creation(self):
    #     self.assertIsNone(self.sdt.get_downtime_file())
    #     self.assertEqual(len(self.sdt), 0)

    # def test_information_after_initialization(self):
    #     self.sdt.initialize()
    #     self.assertEquals(os.path.basename(self.sdt.get_downtime_file()), "scheduled_downtime.db")
    #     self.assertEqual(len(self.sdt), 31)
    #     self.check_downtime(self.sdt.get_downtimes(0), 158, 7, "general maintenance")
    #     self.check_downtime(self.sdt.get_downtimes(-1), 7242, 7, "general maintenance")

    # def test_alternate_db(self):
    #     downtime_dbfile = "alternate_scheduled_downtime.db"

    #     downtime_table = []
    #     downtime_table.append("night INTEGER PRIMARY KEY")
    #     downtime_table.append("duration INTEGER")
    #     downtime_table.append("activity TEXT")

    #     with sqlite3.connect(downtime_dbfile) as conn:
    #         cur = conn.cursor()
    #         cur.execute("DROP TABLE IF EXISTS Downtime")
    #         cur.execute("CREATE TABLE Downtime({})".format(",".join(downtime_table)))
    #         cur.execute("INSERT INTO Downtime VALUES(?, ?, ?)", (100, 7, "something to do"))
    #         cur.close()

    #     self.sdt.initialize(downtime_dbfile)
    #     self.assertEqual(len(self.sdt), 1)
    #     self.check_downtime(self.sdt.get_downtimes(0), 100, 7, "something to do")

    #     os.remove(downtime_dbfile)

    # def test_call(self):
    #     self.sdt.initialize()
    #     self.check_downtime(self.sdt(), 158, 7, "general maintenance")
    #     self.assertEqual(len(self.sdt), 30)
