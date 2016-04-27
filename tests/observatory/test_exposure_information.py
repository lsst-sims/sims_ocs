import unittest

from lsst.sims.ocs.observatory import ExposureInformation

class ExposureInformationTest(unittest.TestCase):

    def test_exposure_information(self):
        exposure = ExposureInformation(1, 0, 15.0, 3)
        self.assertEqual(len(exposure._fields), 4)
        self.assertEqual(exposure.exposureId, 1)
        self.assertEqual(exposure.exposureNum, 0)
        self.assertEqual(exposure.exposureTime, 15.0)
        self.assertEqual(exposure.ObsHistory_observationId, 3)
