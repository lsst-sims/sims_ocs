import collections

__all__ = ["ProposalHistory", "ProposalInfo"]

"""Simple tuple for handling proposal information.
"""
ProposalInfo = collections.namedtuple("ProposalInfo", ["propId", "propName", "propType"])

"""Simple tuple for handling proposal history information.
"""
ProposalHistory = collections.namedtuple("ProposalHistory", ["propHistId", "Proposal_propId", "proposalValue",
                                                             "ObsHistory_observationId"])
