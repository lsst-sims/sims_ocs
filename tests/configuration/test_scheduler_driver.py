import unittest

from lsst.ts.schedulerConfig import SchedulerDriver

class SchedulerDriverTest(unittest.TestCase):

    def setUp(self):
        self.sched_driver = SchedulerDriver()

    def test_basic_information_after_creation(self):
        self.assertTrue(self.sched_driver.coadd_values)
        self.assertTrue(self.sched_driver.time_balancing)
        self.assertEqual(self.sched_driver.timecost_time_max, 150.0)
        self.assertEqual(self.sched_driver.timecost_time_ref, 5.0)
        self.assertEqual(self.sched_driver.timecost_cost_ref, 0.3)
        self.assertEqual(self.sched_driver.timecost_weight, 1.0)
        self.assertEqual(self.sched_driver.filtercost_weight, 1.0)
        self.assertEqual(self.sched_driver.propboost_weight, 1.0)
        self.assertEqual(self.sched_driver.night_boundary, -12.0)
        self.assertEqual(self.sched_driver.new_moon_phase_threshold, 20.0)
        self.assertFalse(self.sched_driver.ignore_sky_brightness)
        self.assertFalse(self.sched_driver.ignore_airmass)
        self.assertFalse(self.sched_driver.ignore_clouds)
        self.assertFalse(self.sched_driver.ignore_seeing)

    def test_propboost_weight_for_bad_value(self):
        self.sched_driver.propboost_weight = -1.0
        with self.assertRaises(ValueError):
            self.sched_driver.validate()
