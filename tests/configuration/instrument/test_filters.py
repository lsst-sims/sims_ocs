import unittest

from lsst.ts.schedulerConfig.instrument import Filters

class FiltersTest(unittest.TestCase):

    def setUp(self):
        self.filters = Filters()

    def test_basic_information_from_creation(self):
        self.assertEqual(self.filters.u_effective_wavelength, 367.0)
        self.assertEqual(self.filters.g_effective_wavelength, 482.5)
        self.assertEqual(self.filters.r_effective_wavelength, 622.2)
        self.assertEqual(self.filters.i_effective_wavelength, 754.5)
        self.assertEqual(self.filters.z_effective_wavelength, 869.1)
        self.assertEqual(self.filters.y_effective_wavelength, 971.0)

    def test_get_effective_wavelength(self):
        self.assertEqual(self.filters.get_effective_wavelength('g'), 482.5)
