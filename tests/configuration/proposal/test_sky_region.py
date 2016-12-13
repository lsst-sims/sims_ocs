import unittest

from lsst.sims.ocs.configuration.proposal import Selection, SelectionList, TimeRange
from lsst.sims.ocs.configuration.proposal import SkyRegion

class SkyRegionTest(unittest.TestCase):

    def setUp(self):
        self.sky_region = SkyRegion()

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.sky_region.selections)
        self.assertIsNotNone(self.sky_region.combiners)
        self.assertIsNone(self.sky_region.time_ranges)
        self.assertIsNone(self.sky_region.selection_mapping)

    def test_selections_assignment(self):
        self.sky_region.selections = {0: Selection()}
        self.assertIsNotNone(self.sky_region.selections)
        self.assertEqual(len(self.sky_region.selections), 1)

    def test_selections_addition(self):
        with self.assertRaises(TypeError):
            self.sky_region.selections[0] = Selection()

    def test_time_ranges_assignment(self):
        self.sky_region.time_ranges = {0: TimeRange()}
        self.assertIsNotNone(self.sky_region.time_ranges)
        self.assertEqual(len(self.sky_region.time_ranges), 1)

    def test_time_ranges_addition(self):
        with self.assertRaises(TypeError):
            self.sky_region.time_ranges[0] = TimeRange()

    def test_selection_mapping_assignment(self):
        self.sky_region.selection_mapping = {0: SelectionList()}
        self.assertIsNotNone(self.sky_region.selection_mapping)
        self.assertEqual(len(self.sky_region.selection_mapping), 1)

    def test_selection_mapping_addition(self):
        with self.assertRaises(TypeError):
            self.sky_region.selection_mapping[0] = SelectionList()
