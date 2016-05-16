import lsst.pex.config as pexConfig

__all__ = ["Selection", "SELECTION_LIMIT_TYPES"]

SELECTION_LIMIT_TYPES = ["RA", "Dec"]

class Selection(pexConfig.Config):
    """Select fields via limits.
    """

    limit_type = pexConfig.Field('Type of coordinate to select.', str)
    minimum_limit = pexConfig.Field('Minimum limit (units=degrees) for field selection.', float)
    maximum_limit = pexConfig.Field('Maximum limit (units=degrees) for field selection.', float)

    def setDefaults(self):
        """Default specification for a selection.
        """

        self.limit_type = "RA"
        self.minimum_limit = 0.0
        self.maximum_limit = 360.0

    def validate(self):
        """Validate configuration parameters.
        """
        pexConfig.Config.validate(self)
        if self.minimum_limit > self.maximum_limit:
            self.minimum_limit, self.maximum_limit = self.maximum_limit, self.minimum_limit
        if self.limit_type not in SELECTION_LIMIT_TYPES:
            raise ValueError("Limit type must be on of: {}".format(SELECTION_LIMIT_TYPES))
