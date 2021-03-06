import collections

__all__ = ["ObsProposalHistory", "ProposalFieldInfo", "ProposalInfo", "TargetProposalHistory"]

"""Simple tuple for handling proposal information.
"""
ProposalInfo = collections.namedtuple("ProposalInfo", ["propId", "propName", "propType"])

"""Simple tuple for handling observation proposal history information.
"""
ObsProposalHistory = collections.namedtuple("ObsProposalHistory", ["propHistId", "Proposal_propId",
                                                                   "proposalValue", "proposalNeed",
                                                                   "proposalBonus", "proposalBoost",
                                                                   "ObsHistory_observationId"])

"""Simple tuple for handling target proposal history information.
"""
TargetProposalHistory = collections.namedtuple("TargetProposalHistory", ["propHistId", "Proposal_propId",
                                                                         "proposalValue", "proposalNeed",
                                                                         "proposalBonus", "proposalBoost",
                                                                         "TargetHistory_targetId"])

"""Simple tuple for handling proposal field information.
"""
ProposalFieldInfo = collections.namedtuple("ProposalFieldInfo", ["propFieldId", "Proposal_propId",
                                                                 "Field_fieldId"])
