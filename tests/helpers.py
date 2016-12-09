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
