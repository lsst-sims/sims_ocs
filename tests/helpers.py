"""Number of SAL put calls used in the configuration communicator.
"""
CONFIG_COMM_PUT_CALLS = 11
"""Current list of all general proposals.
"""
GEN_PROPS = ["GalacticPlane", "NorthEclipticSpur", "SouthCelestialPole", "WideFastDeep"]
"""Number of currently defined general proposals.
"""
NUM_GEN_PROPS = len(GEN_PROPS)
"""Constant for handling extra put calls beyond a single general proposal.
"""
CONFIG_GEN_PROPS = NUM_GEN_PROPS - 1
"""A set of sky brightness values.
"""
SKY_BRIGHTNESS = {'u': [16.0], 'g': [17.0], 'r': [18.0], 'i': [19.0], 'z': [20.0], 'y': [21.0]}
"""A set of target information.
"""
TARGET_INFO = {'airmass': [1.1], 'altitude': [0.5], 'azimuth': [0.5]}
"""A set of moon and sun information.
"""
MOON_SUN_INFO = {'moonRA': 30.0, 'moonDec': 10.0, 'moonAlt': -2.0, 'moonAz': 135.0, 'moonPhase': 0.3,
                 'moonDist': [80.0], 'sunRA': 310.0, 'sunDec': 5.0, 'sunAlt': -24.0, 'sunAz': 285.0,
                 'solarElong': [150.0]}
