import logging
try:
    from unittest import mock
except ImportError:
    import mock
import unittest

from lsst.sims.ocs.configuration import Downtime
from lsst.sims.ocs.kernel import DowntimeHandler

class DowntimeHandlerTest(unittest.TestCase):

    def setUp(self):
        self.dh = DowntimeHandler()
        self.conf = Downtime()
        logging.getLogger().setLevel(logging.WARN)

        patcher1 = mock.patch("lsst.sims.ocs.downtime.scheduled_downtime.ScheduledDowntime", spec=True)
        self.addCleanup(patcher1.stop)
        self.mock_scheduled_downtime = patcher1.start()
        patcher2 = mock.patch("lsst.sims.ocs.downtime.unscheduled_downtime.UnscheduledDowntime", spec=True)
        self.addCleanup(patcher2.stop)
        self.mock_unscheduled_downtime = patcher2.start()

    def initialize(self):
        self.dh.initialize(self.conf)

    def initialize_mocks(self):
        self.dh.scheduled = self.mock_scheduled_downtime
        self.dh.unscheduled = self.mock_unscheduled_downtime

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.dh.scheduled)
        self.assertIsNotNone(self.dh.unscheduled)
        self.assertEqual(len(self.dh.downtime_days), 0)

    def test_information_after_initialization(self):
        self.initialize()
        self.assertGreater(len(self.dh.scheduled), 0)
        self.assertGreater(len(self.dh.unscheduled), 0)

    @mock.patch("time.time")
    def test_information_with_alternate_unscheduled_downtime_seed(self, mock_time):
        alt_seed = 1466094470
        mock_time.return_value = alt_seed
        self.conf.unscheduled_downtime_use_random_seed = True
        self.initialize()
        self.assertGreater(len(self.dh.scheduled), 0)
        self.assertGreater(len(self.dh.unscheduled), 0)
        self.assertEqual(self.conf.unscheduled_downtime_random_seed, alt_seed)

    def test_no_more_downtime(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = None
        self.mock_unscheduled_downtime.return_value = None
        self.assertEqual(self.dh.get_downtime(100), 0)

    def test_no_downtime(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (110, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (130, 1, "minor event")
        self.assertEqual(self.dh.get_downtime(100), 0)
        self.assertIsNone(self.dh.current_scheduled)
        self.assertIsNotNone(self.dh.current_unscheduled)

    def test_no_overlap_scheduled_before_unscheduled(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (100, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (130, 1, "minor event")
        self.assertEqual(self.dh.get_downtime(100), 7)
        self.assertEqual(self.dh.get_downtime(101), 6)
        self.dh.downtime_days.difference_update(set(list(range(102, 107))))
        self.assertEqual(self.dh.get_downtime(107), 0)
        self.assertIsNone(self.dh.current_scheduled)
        self.assertIsNotNone(self.dh.current_unscheduled)

    def test_no_overlap_unscheduled_before_scheduled(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (110, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (100, 1, "minor event")
        self.assertEqual(self.dh.get_downtime(100), 1)
        self.assertEqual(self.dh.get_downtime(101), 0)
        self.assertIsNotNone(self.dh.current_scheduled)
        self.assertIsNone(self.dh.current_unscheduled)

    def test_full_overlap_unscheduled_in_scheduled(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (100, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (102, 3, "intermediate event")
        self.assertEqual(self.dh.get_downtime(100), 7)
        self.assertEqual(self.dh.get_downtime(101), 6)
        self.dh.downtime_days.difference_update(set(list(range(102, 107))))
        self.assertEqual(self.dh.get_downtime(107), 0)
        self.assertIsNone(self.dh.current_scheduled)
        self.assertIsNone(self.dh.current_unscheduled)

    def test_full_overlap_scheduled_in_unscheduled(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (103, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (100, 14, "catastrophic event")
        self.assertEqual(self.dh.get_downtime(100), 14)
        self.assertEqual(self.dh.get_downtime(101), 13)
        self.dh.downtime_days.difference_update(set(list(range(102, 114))))
        self.assertEqual(self.dh.get_downtime(114), 0)
        self.assertIsNone(self.dh.current_scheduled)
        self.assertIsNone(self.dh.current_unscheduled)

    def test_partial_overlap_unscheduled_after_scheduled(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (100, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (106, 3, "intermediate event")
        self.assertEqual(self.dh.get_downtime(100), 9)
        self.assertEqual(self.dh.get_downtime(101), 8)
        self.dh.downtime_days.difference_update(set(list(range(102, 109))))
        self.assertEqual(self.dh.get_downtime(109), 0)
        self.assertIsNone(self.dh.current_scheduled)
        self.assertIsNone(self.dh.current_unscheduled)

    def test_partial_overlap_scheduled_after_unscheduled(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.return_value = (101, 7, "routine maintanence")
        self.mock_unscheduled_downtime.return_value = (100, 3, "intermediate event")
        self.assertEqual(self.dh.get_downtime(100), 8)
        self.assertEqual(self.dh.get_downtime(101), 7)
        self.assertEqual(self.dh.get_downtime(102), 6)
        self.dh.downtime_days.difference_update(set(list(range(103, 108))))
        self.assertEqual(self.dh.get_downtime(108), 0)
        self.assertIsNone(self.dh.current_scheduled)
        self.assertIsNone(self.dh.current_unscheduled)

    def test_downtime_cycling(self):
        self.initialize_mocks()
        self.mock_scheduled_downtime.side_effect = ((100, 7, "routine maintanence"),
                                                    (122, 7, "routine maintanence"),
                                                    None, None)
        self.mock_unscheduled_downtime.side_effect = ((109, 1, "minor event"),
                                                      (120, 3, "intermediate event"),
                                                      None, None)

        self.assertEqual(self.dh.get_downtime(100), 7)
        self.assertEqual(self.dh.get_downtime(101), 6)
        self.dh.downtime_days.difference_update(set(list(range(102, 107))))
        self.assertEqual(self.dh.get_downtime(107), 0)
        self.assertEqual(self.dh.get_downtime(108), 0)
        self.assertEqual(self.dh.get_downtime(109), 1)
        self.assertEqual(self.dh.get_downtime(110), 0)
        self.assertEqual(self.dh.get_downtime(120), 9)
        self.dh.downtime_days.difference_update(set(list(range(121, 129))))
        self.assertEqual(self.dh.get_downtime(129), 0)
        self.assertEqual(self.dh.get_downtime(130), 0)

    @mock.patch("lsst.sims.ocs.database.socs_db.SocsDatabase", spec=True)
    def test_database_write(self, mock_db):
        self.initialize()
        self.dh.write_downtime_to_db(mock_db)
        self.assertEqual(mock_db.append_data.call_count, 158 + 31)
        self.assertEqual(mock_db.write.call_count, 1)
        self.assertEqual(mock_db.clear_data.call_count, 1)
