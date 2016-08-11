import collections

__all__ = ["ProposalInfo"]

"""Simple tuple for handling proposal information.
"""
ProposalInfo = collections.namedtuple("ProposalInfo", ["propId", "propName", "propType"])
