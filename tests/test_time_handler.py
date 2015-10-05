from datetime import datetime
import unittest

import lsst.sims.ocs.kernel.time_handler as th
from lsst.sims.ocs.kernel.time_handler import TimeHandler

class TimeHandlerTest(unittest.TestCase):

    def setUp(self):
        self.start_date = "2020-05-24"
        self.th = TimeHandler(self.start_date)

    def test_initial_creation(self):
        self.assertEqual(self.th.initial_dt, datetime(2020, 5, 24))

    def test_bad_date_string(self):
        with self.assertRaises(ValueError):
            TimeHandler("18-09-15")

    def test_return_initial_timestamp(self):
        truth_timestamp = (datetime(2020, 5, 24) - datetime(1970, 1, 1)).total_seconds()
        self.assertEqual(self.th.initial_timestamp, truth_timestamp)

    def test_time_adjustment_seconds(self):
        self.th.update_time(30.0, "seconds")
        self.assertEqual(self.th.current_dt, datetime(2020, 5, 24, 0, 0, 30))

    def test_time_adjustment_hours(self):
        self.th.update_time(3.5, "hours")
        self.assertEqual(self.th.current_dt, datetime(2020, 5, 24, 3, 30, 0))

    def test_time_adjustment_days(self):
        self.th.update_time(4, "days")
        self.assertEqual(self.th.current_dt, datetime(2020, 5, 28))

    def test_multiple_time_adjustments(self):
        for i in range(3):
            self.th.update_time(30.0, "seconds")
        self.assertEqual(self.th.current_dt, datetime(2020, 5, 24, 0, 1, 30))

    def test_timestamp_after_time_adjustment(self):
        truth_timestamp = (datetime(2020, 5, 24, 0, 0, 30) - datetime(1970, 1, 1)).total_seconds()
        self.th.update_time(30.0, "seconds")
        self.assertEqual(self.th.current_timestamp, truth_timestamp)
        self.assertNotEqual(self.th.current_timestamp, self.th.initial_timestamp)

    def test_current_timestamp_string(self):
        self.assertEqual(self.th.current_timestring, "2020-05-24T00:00:00")

    def test_time_span_less_than_time_elapsed(self):
        self.th.update_time(10, "days")
        self.assertFalse(self.th.has_time_elapsed(9 * th.SECONDS_IN_DAY))

    def test_time_span_is_greater_than_time_elapsed(self):
        self.th.update_time(10, "days")
        self.assertTrue(self.th.has_time_elapsed(11 * th.SECONDS_IN_DAY))
