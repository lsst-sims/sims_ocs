import unittest

from lsst.sims.ocs.configuration.obs_site import ObservingSite

class ObservingSiteTest(unittest.TestCase):

    def setUp(self):
        self.obs_site = ObservingSite()
        self.truth_latitude = -30.2444
        self.truth_longitude = -70.7494

    def test_basic_information_from_creation(self):
        self.assertEqual(self.obs_site.name, "Cerro Pachon")
        self.assertEqual(self.obs_site.latitude, self.truth_latitude)
        self.assertEqual(self.obs_site.longitude, self.truth_longitude)
        self.assertEqual(self.obs_site.height, 2650.)
        self.assertEqual(self.obs_site.pressure, 750.0)
        self.assertEqual(self.obs_site.temperature, 11.5)
        self.assertEqual(self.obs_site.relativeHumidity, 0.4)

    def test_radians_return_for_latlon(self):
        import math
        self.assertEqual(self.obs_site.latitude_rad, math.radians(self.truth_latitude))
        self.assertEqual(self.obs_site.longitude_rad, math.radians(self.truth_longitude))
