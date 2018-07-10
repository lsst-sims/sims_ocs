import math
import unittest

from lsst.ts.schedulerConfig.proposal import Selection

class SelectionTest(unittest.TestCase):

    def setUp(self):
        self.selection = Selection()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.selection.limit_type, "RA")
        self.assertEqual(self.selection.minimum_limit, 0.0)
        self.assertEqual(self.selection.maximum_limit, 360.0)
        self.assertTrue(math.isnan(self.selection.bounds_limit))

    def test_bad_limit_type(self):
        self.selection.limit_type = "None"
        with self.assertRaises(ValueError):
            self.selection.validate()
