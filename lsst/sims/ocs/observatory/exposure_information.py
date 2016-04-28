import collections

__all__ = ["TargetExposure"]

"""Simple tuple for handling a single target exposure's information
"""
TargetExposure = collections.namedtuple("TargetExposure", ["exposureId", "exposureNum", "exposureTime",
                                                           "TargetHistory_targetId"])
