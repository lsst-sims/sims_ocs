import lsst.pex.config as pexConfig

__all__ = ["Selection", "SELECTION_LIMIT_TYPES"]

SELECTION_LIMIT_TYPES = ["RA", "Dec", "GL", "GB", "EL", "EB", "GP"]
"""Selection types for sky regions and sky exclusions.

RA
    right-ascension
Dec
    declination
GL
    galactic longitude
GB
    galactic latitude
EL
    ecliptic longitude
EB
    ecliptic latitude
GP
    galactic plane
"""

class Selection(pexConfig.Config):
    """Select fields via limits.
    """

    limit_type = pexConfig.Field('Type of coordinate to select.', str)
    minimum_limit = pexConfig.Field('Minimum limit (units=degrees) for field selection.', float)
    maximum_limit = pexConfig.Field('Maximum limit (units=degrees) for field selection.', float)
    bounds_limit = pexConfig.Field('Boundary limit (units=degrees) for a sloping envelope selection.', float)

    def setDefaults(self):
        """Default specification for a selection.
        """

        self.limit_type = "RA"
        self.minimum_limit = 0.0
        self.maximum_limit = 360.0
        self.bounds_limit = float('nan')

    def validate(self):
        """Validate configuration parameters.
        """
        pexConfig.Config.validate(self)
        if self.limit_type not in SELECTION_LIMIT_TYPES:
            raise ValueError("Limit type must be on of: {}".format(SELECTION_LIMIT_TYPES))
