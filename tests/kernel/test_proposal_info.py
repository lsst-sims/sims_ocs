import unittest

from lsst.sims.ocs.kernel import ObsProposalHistory, ProposalFieldInfo, ProposalInfo, TargetProposalHistory

class ProposalInformationTest(unittest.TestCase):

    def test_proposal_info(self):
        pi = ProposalInfo(1, "TestProposal", "General")
        self.assertEqual(len(pi._fields), 3)
        self.assertEqual(pi.propId, 1)
        self.assertEqual(pi.propName, "TestProposal")
        self.assertEqual(pi.propType, "General")

class ObsProposalHistoryTest(unittest.TestCase):

    def test_observation_proposal_history(self):
        ph = ObsProposalHistory(1, 2, 1.32, 0.5, 0.82, 0.2, 10)
        self.assertEqual(len(ph._fields), 7)
        self.assertEqual(ph.propHistId, 1)
        self.assertEqual(ph.Proposal_propId, 2)
        self.assertEqual(ph.proposalValue, 1.32)
        self.assertEqual(ph.proposalNeed, 0.5)
        self.assertEqual(ph.proposalBonus, 0.82)
        self.assertEqual(ph.proposalBoost, 0.2)
        self.assertEqual(ph.ObsHistory_observationId, 10)

class TargetProposalHistoryTest(unittest.TestCase):

    def test_target_proposal_history(self):
        ph = TargetProposalHistory(1, 2, 1.32, 0.5, 0.82, 0.2, 10)
        self.assertEqual(len(ph._fields), 7)
        self.assertEqual(ph.propHistId, 1)
        self.assertEqual(ph.Proposal_propId, 2)
        self.assertEqual(ph.proposalValue, 1.32)
        self.assertEqual(ph.proposalNeed, 0.5)
        self.assertEqual(ph.proposalBonus, 0.82)
        self.assertEqual(ph.proposalBoost, 0.2)
        self.assertEqual(ph.TargetHistory_targetId, 10)

class ProposalFieldInformationTest(unittest.TestCase):

    def test_proposal_field_info(self):
        pfi = ProposalFieldInfo(1, 4, 1545)
        self.assertEqual(len(pfi.fields), 3)
        self.assertEqual(pfi.propFieldId, 1)
        self.assertEqual(pfi.propId, 4)
        self.assertEqual(pfi.fieldId, 1545)
