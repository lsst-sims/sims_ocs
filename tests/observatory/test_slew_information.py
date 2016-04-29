import unittest

from lsst.sims.ocs.observatory import SlewHistory, SlewState

class SlewInformationTest(unittest.TestCase):

    def test_slew_history_information(self):
        sh = SlewHistory(1, 2922, 2925, 6.0, 1.0, 1)
        self.assertEqual(len(sh._fields), 6)
        self.assertEqual(sh.slewCount, 1)
        self.assertEqual(sh.startDate, 2922)
        self.assertEqual(sh.endDate, 2925)
        self.assertEqual(sh.slewTime, 6.0)
        self.assertEqual(sh.slewDistance, 1.0)
        self.assertEqual(sh.ObsHistory_observationId, 1)

    def test_slew_state_information(self):
        ss = SlewState(1, 1640995200.0, 1.000, -3.000, "False", 34.1, 155.4, 0.5, 35.2, 156.3, 34.6, 155.6,
                       1.0, 0.5, "r", 1)
        self.assertEqual(len(ss._fields), 16)
        self.assertEqual(ss.slewStateId, 1)
        self.assertEqual(ss.slewStateDate, 1640995200.0)
        self.assertEqual(ss.targetRA, 1.000)
        self.assertEqual(ss.targetDec, -3.000)
        self.assertEqual(ss.tracking, "False")
        self.assertEqual(ss.altitude, 34.1)
        self.assertEqual(ss.azimuth, 155.4)
        self.assertEqual(ss.posAngle, 0.5)
        self.assertEqual(ss.domeAlt, 35.2)
        self.assertEqual(ss.domeAz, 156.3)
        self.assertEqual(ss.telAlt, 34.6)
        self.assertEqual(ss.telAz, 155.6)
        self.assertEqual(ss.rotTelPos, 1.0)
        self.assertEqual(ss.rotSkyPos, 0.5)
        self.assertEqual(ss.filter, 'r')
        self.assertEqual(ss.SlewHistory_slewCount, 1)
