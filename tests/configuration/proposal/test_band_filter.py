import unittest

from lsst.sims.ocs.configuration.proposal import BandFilter

class BandFilterTest(unittest.TestCase):

    def setUp(self):
        self.band_filter = BandFilter()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.band_filter.name, 'u')
        self.assertEqual(self.band_filter.num_visits, 10)
        self.assertEqual(self.band_filter.num_grouped_visits, 1)
        self.assertEqual(self.band_filter.bright_limit, 21.0)
        self.assertEqual(self.band_filter.dark_limit, 30.0)
        self.assertEqual(self.band_filter.max_seeing, 2.0)
        self.assertListEqual(list(self.band_filter.exposures), [15.0, 15.0])

    def test_reversed_bright_dark(self):
        self.band_filter.bright_limit = 29.0
        self.band_filter.dark_limit = 24.0
        self.band_filter.validate()
        self.assertEqual(self.band_filter.bright_limit, 24.0)
        self.assertEqual(self.band_filter.dark_limit, 29.0)
