import collections

__all__ = ["ExposureInformation"]

"""Simple tuple for handling a single exposure's information
"""
ExposureInformation = collections.namedtuple("ExposureInformation", ["exposureID", "exposureNum",
                                                                     "exposureTime",
                                                                     "ObsHistory_observationID"])
