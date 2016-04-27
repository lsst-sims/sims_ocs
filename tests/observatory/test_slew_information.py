import unittest

from lsst.sims.ocs.observatory import SlewHistory

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
