import unittest

from lsst.sims.ocs.observatory import ObsExposure, TargetExposure

class ExposureInformationTest(unittest.TestCase):

    def test_target_exposure_information(self):
        exposure = TargetExposure(1, 0, 15.0, 3)
        self.assertEqual(len(exposure._fields), 4)
        self.assertEqual(exposure.exposureId, 1)
        self.assertEqual(exposure.exposureNum, 0)
        self.assertEqual(exposure.exposureTime, 15.0)
        self.assertEqual(exposure.TargetHistory_targetId, 3)

    def test_observation_exposure_information(self):
        exposure = ObsExposure(1, 0, 15.0, 2922, 3)
        self.assertEqual(len(exposure._fields), 5)
        self.assertEqual(exposure.exposureId, 1)
        self.assertEqual(exposure.exposureNum, 0)
        self.assertEqual(exposure.exposureTime, 15.0)
        self.assertEqual(exposure.exposureStartTime, 2922),
        self.assertEqual(exposure.ObsHistory_observationId, 3)
