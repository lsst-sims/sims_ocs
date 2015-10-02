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

    def test_radians_return_for_latlon(self):
        import math
        self.assertEqual(self.obs_site.latitude_rads, math.radians(self.truth_latitude))
        self.assertEqual(self.obs_site.longitude_rads, math.radians(self.truth_longitude))
