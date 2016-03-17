import collections

__all__ = ["SlewHistory"]

"""Simple tuple for handling slew history information.
"""
SlewHistory = collections.namedtuple("SlewHistory", "slewCount startDate endDate slewTime slewDistance "
                                     "ObsHistory_observationID")
