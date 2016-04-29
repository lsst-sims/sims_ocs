import collections

__all__ = ["SlewActivity", "SlewHistory", "SlewState"]

"""Simple tuple for handling slew history information.
"""
SlewHistory = collections.namedtuple("SlewHistory", ["slewCount", "startDate", "endDate", "slewTime",
                                                     "slewDistance", "ObsHistory_observationId"])

"""Simple tuple for handling slew state information.
"""
SlewState = collections.namedtuple("SlewState", ["slewStateId", "slewStateDate", "targetRA", "targetDec",
                                                 "tracking", "altitude", "azimuth", "paraAngle", "domeAlt",
                                                 "domeAz", "telAlt", "telAz", "rotTelPos", "rotSkyPos",
                                                 "filter", "SlewHistory_slewCount"])

"""Simple tuple for handling slew activity information.
"""
SlewActivity = collections.namedtuple("SlewActivity", ["slewActivityId", "activity", "activityDelay",
                                                       "inCriticalPath", "SlewHistory_slewCount"])
