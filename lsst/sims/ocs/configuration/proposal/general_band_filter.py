import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BandFilter

__all__ = ["GeneralBandFilter"]

class GeneralBandFilter(BandFilter):
    """Configuration for a general proposal filter.
    """
    num_visits = pexConfig.Field('The number of requested visits for the filter.', int)
    num_grouped_visits = pexConfig.Field('The number of grouped (in a night) visits for the filter.', int)

    def setDefaults(self):
        """Default specification for a general proposal filter.
        """
        BandFilter.setDefaults(self)
        self.num_visits = 10
        self.num_grouped_visits = 1

    def validate(self):
        """Validate configuration parameters.
        """
        BandFilter.validate(self)
