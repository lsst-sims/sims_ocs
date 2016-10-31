import collections

__all__ = ["ObsProposalHistory", "ProposalInfo"]

"""Simple tuple for handling proposal information.
"""
ProposalInfo = collections.namedtuple("ProposalInfo", ["propId", "propName", "propType"])

"""Simple tuple for handling observation proposal history information.
"""
ObsProposalHistory = collections.namedtuple("ObsProposalHistory", ["propHistId", "Proposal_propId",
                                                                   "proposalValue", "proposalNeed",
                                                                   "proposalBonus", "proposalBoost",
                                                                   "ObsHistory_observationId"])
