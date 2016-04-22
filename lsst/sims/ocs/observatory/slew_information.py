import collections

__all__ = ["SlewHistory", "SlewState"]

"""Simple tuple for handling slew history information.
"""
SlewHistory = collections.namedtuple("SlewHistory", ["slewCount", "startDate", "endDate", "slewTime",
                                                     "slewDistance", "ObsHistory_observationID"])

SlewState = collections.namedtuple("SlewState", ["slewStateDate", "targetRA", "targetDec",
                                                 "tracking", "altitude", "azimuth", "posAngle", "domeAlt",
                                                 "domeAz", "telAlt", "telAz", "rotTelPos", "rotSkyPos",
                                                 "filter", "state", "SlewHistory_slewCount"])
