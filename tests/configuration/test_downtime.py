import unittest

from lsst.sims.ocs.configuration.downtime import Downtime

class DowntimeTest(unittest.TestCase):

    def setUp(self):
        self.down = Downtime()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.down.scheduled_downtime_db, "")
        self.assertFalse(self.down.unscheduled_downtime_use_random_seed)
        self.assertEqual(self.down.unscheduled_downtime_random_seed, -1)
