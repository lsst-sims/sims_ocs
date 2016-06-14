import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import Selection

__all__ = ["SkyExclusion"]

class SkyExclusion(pexConfig.Config):
    """Configuration for a proposal's sky exclusions.
    """

    dec_window = pexConfig.Field('Angle (units=degrees) around the observing site\'s latitude for which to '
                                 'create a Declination window for field selection.', float)

    selections = pexConfig.ConfigDictField('A list of type selections for sky exclusion '
                                           'determination. Currently, only GP is supported.',
                                           int, Selection)

    def setDefaults(self):
        """Default specification for a sky exclusions.
        """
        self.dec_window = 90.0
        self.selections = {}
