import unittest

from lsst.sims.ocs.configuration.proposal import TimeRange

class TimeRangeTest(unittest.TestCase):

    def test_basic_information_after_creation(self):
        time_range = TimeRange()
        self.assertEqual(time_range.start, 0)
        self.assertEqual(time_range.end, 0)

    def test_assigned_information(self):
        time_range = TimeRange()
        time_range.start = 1
        time_range.end = 1533
        self.assertEqual(time_range.start, 1)
        self.assertEqual(time_range.end, 1533)

    def test_after_validation(self):
        time_range = TimeRange()
        time_range.start = 1533
        time_range.end = 1
        time_range.validate()
        self.assertEqual(time_range.start, 1)
        self.assertEqual(time_range.end, 1533)
