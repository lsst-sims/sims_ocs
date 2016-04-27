import collections

__all__ = ["ExposureInformation"]

"""Simple tuple for handling a single exposure's information
"""
ExposureInformation = collections.namedtuple("ExposureInformation", ["exposureId", "exposureNum",
                                                                     "exposureTime",
                                                                     "ObsHistory_observationId"])
