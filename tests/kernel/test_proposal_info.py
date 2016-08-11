import unittest

from lsst.sims.ocs.kernel import ProposalInfo

class ProposalInformationTest(unittest.TestCase):

    def test_proposal_info(self):
        pi = ProposalInfo(1, "TestProposal", "AreaDistribution")
        self.assertEqual(len(pi._fields), 3)
        self.assertEqual(pi.propId, 1)
        self.assertEqual(pi.propName, "TestProposal")
        self.assertEqual(pi.propType, "AreaDistribution")
