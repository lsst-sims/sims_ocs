import unittest

from lsst.sims.ocs.kernel import ProposalHistory, ProposalInfo

class ProposalInformationTest(unittest.TestCase):

    def test_proposal_info(self):
        pi = ProposalInfo(1, "TestProposal", "AreaDistribution")
        self.assertEqual(len(pi._fields), 3)
        self.assertEqual(pi.propId, 1)
        self.assertEqual(pi.propName, "TestProposal")
        self.assertEqual(pi.propType, "AreaDistribution")

class ProposalHistoryTest(unittest.TestCase):

    def test_proposal_history(self):
        ph = ProposalHistory(1, 2, 1.32, 10)
        self.assertEqual(len(ph._fields), 4)
        self.assertEqual(ph.propHistId, 1)
        self.assertEqual(ph.Proposal_propId, 2)
        self.assertEqual(ph.proposalValue, 1.32)
        self.assertEqual(ph.ObsHistory_observationId, 10)
