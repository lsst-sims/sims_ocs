import unittest

from lsst.sims.ocs.configuration import SchedulerDriver

class SchedulerDriverTest(unittest.TestCase):

    def setUp(self):
        self.sched_driver = SchedulerDriver()

    def test_basic_information_after_creation(self):
        self.assertTrue(self.sched_driver.coadd_values)
        self.assertEqual(self.sched_driver.timebonus_tmax, 200.0)
        self.assertEqual(self.sched_driver.timebonus_bmax, 10.0)
        self.assertEqual(self.sched_driver.timebonus_slope, 2.26)
        self.assertEqual(self.sched_driver.night_boundary, -12.0)
