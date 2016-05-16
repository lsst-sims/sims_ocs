import lsst.pex.config as pexConfig

__all__ = ["GalacticExclusion"]

class GalacticExclusion(pexConfig.Config):
    """Configuration of a galactic exclusion zone.
    """

    taper_l = pexConfig.Field('The half width in galactic latitude (units=degrees) at the galactic longitude '
                              'specified by taper_b.', float)
    taper_b = pexConfig.Field('The galactic longitude (units=degrees) where taper_l is in effect.', float)
    peak_l = pexConfig.Field('The half width in galactic latitude (units=degrees) at the galactic longitude '
                             'of 0.', float)

    def setDefaults(self):
        """Default specification for galactic exclusion zone.
        """
        self.taper_l = 2.0
        self.taper_b = 180.0
        self.peak_l = 20.0
