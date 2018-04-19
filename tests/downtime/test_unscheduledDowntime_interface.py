import logging
try:
    from unittest import mock
except ImportError:
    import mock
import unittest

from lsst.sims.ocs.downtime.unscheduledDowntime_interface import UnscheduledDowntimeInterface

class UnscheduledDowntimeTest(unittest.TestCase):

    def setUp(self):
        self.usdt = UnscheduledDowntimeInterface()
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
    #     self.assertEqual(self.usdt.get_seed(), 1516231120)
    #     self.assertEqual(len(self.usdt), 0)

    # def test_information_after_iniitialization(self):
    #     self.usdt.initialize()
    #     self.assertEqual(len(self.usdt), 158)
    #     self.assertEqual(self.usdt.total_downtime(), 322)
    #     self.check_downtime(self.usdt.get_downtimes(0), 29, 1, "minor event")
    #     self.check_downtime(self.usdt.get_downtimes(-1), 7228, 3, "intermediate event")

    # @mock.patch("time.time")
    # def test_alternate_seed(self, mock_time):
    #     mock_time.return_value = 1466094470
    #     self.usdt.initialize(use_random_seed=True)
    #     self.assertEqual(len(self.usdt), 166)
    #     self.assertEqual(self.usdt.total_downtime(), 328)
    #     self.check_downtime(self.usdt.get_downtimes(0), 28, 1, "minor event")
    #     self.check_downtime(self.usdt.get_downtimes(-1), 7248, 3, "intermediate event")

    # def test_alternate_seed_with_override(self):
    #     self.usdt.initialize(use_random_seed=True, random_seed=1466094470)
    #     self.assertEqual(len(self.usdt), 166)
    #     self.assertEqual(self.usdt.total_downtime(), 328)
    #     self.check_downtime(self.usdt.get_downtimes(0), 28, 1, "minor event")
    #     self.check_downtime(self.usdt.get_downtimes(-1), 7248, 3, "intermediate event")

    # def test_call(self):
    #     self.usdt.initialize()
    #     self.check_downtime(self.usdt(), 29, 1, "minor event")
    #     self.assertEqual(len(self.usdt), 157)
