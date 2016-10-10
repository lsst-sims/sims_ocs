import unittest

from lsst.sims.ocs.configuration import SchedulerDriver

class SchedulerDriverTest(unittest.TestCase):

    def setUp(self):
        self.sched_driver = SchedulerDriver()

    def test_basic_information_after_creation(self):
        self.assertTrue(self.sched_driver.coadd_values)
        self.assertTrue(self.sched_driver.time_balancing)
        self.assertEqual(self.sched_driver.timebonus_tmax, 200.0)
        self.assertEqual(self.sched_driver.timebonus_bmax, 10.0)
        self.assertEqual(self.sched_driver.timebonus_slope, 5.0)
        self.assertEqual(self.sched_driver.night_boundary, -12.0)
        self.assertFalse(self.sched_driver.ignore_sky_brightness)
        self.assertFalse(self.sched_driver.ignore_airmass)
        self.assertFalse(self.sched_driver.ignore_clouds)
        self.assertFalse(self.sched_driver.ignore_seeing)
