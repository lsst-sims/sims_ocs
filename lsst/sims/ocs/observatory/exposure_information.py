import collections

__all__ = ["ObsExposure", "TargetExposure"]

"""Simple tuple for handling a single target exposure's information
"""
TargetExposure = collections.namedtuple("TargetExposure", ["exposureId", "exposureNum", "exposureTime",
                                                           "TargetHistory_targetId"])

"""Simple tuple for handling a single observation exposure's information
"""
ObsExposure = collections.namedtuple("ObsExposure", ["exposureId", "exposureNum", "exposureTime",
                                                     "exposureStartTime", "ObsHistory_observationId"])
