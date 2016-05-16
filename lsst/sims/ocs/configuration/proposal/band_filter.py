import lsst.pex.config as pexConfig

__all__ = ["BandFilter"]

class BandFilter(pexConfig.Config):
    """Configuration for a proposal filter.
    """
    name = pexConfig.Field('Band name of the filter.', str)
    num_visits = pexConfig.Field('The number of requested visits for the filter.', int)
    bright_limit = pexConfig.Field('Brightest magnitude limit for filter.', float)
    dark_limit = pexConfig.Field('Darkest magnitude limit for filter.', float)
    max_seeing = pexConfig.Field('The maximum seeing limit for filter', float)
    exposures = pexConfig.ListField('The list of exposure times (units=seconds) for the filter', float)

    def setDefaults(self):
        """Default specification for a filter.
        """
        self.name = "u"
        self.num_visits = 10
        self.bright_limit = 21.0
        self.dark_limit = 30.0
        self.max_seeing = 2.0
        self.exposures = [15.0, 15.0]

    def validate(self):
        """Validate configuration parameters.
        """
        pexConfig.Config.validate(self)
        if self.bright_limit > self.dark_limit:
            self.bright_limit, self.dark_limit = self.dark_limit, self.bright_limit
