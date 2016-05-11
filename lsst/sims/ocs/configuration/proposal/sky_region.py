import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import GalacticExclusion, Selection

__all__ = ["SkyRegion"]

class SkyRegion(pexConfig.Config):
    """Configuration for a proposal's sky region of interest.
    """

    twilight_boundary = pexConfig.Field('The sun altitude (units=degrees) for twilight consideration.', float)

    delta_lst = pexConfig.Field('LST extent (units=degrees) before sunset LST (-) and after sunrise LST (+) '
                                'for providing a region of the sky to select.', float)
    dec_window = pexConfig.Field('Angle (units=degrees) around the observing site\'s latitude for which to '
                                 'create a Declination window for field selection.', float)

    limit_selections = pexConfig.ConfigDictField('A list of type selections for sky region determination.',
                                                 str, Selection)

    use_galactic_exclusion = pexConfig.Field('Use the galactic exclusion zone when selection fields.', bool)
    galactic_exclusion = pexConfig.ConfigField('Parameters for setting a galactic exclusion zone.',
                                               GalacticExclusion)

    def setDefaults(self):
        """Default specification for a sky region.
        """
        self.twilight_boundary = -12.0
        self.delta_lst = 30.0
        self.dec_window = 90.0
        self.use_galactic_exclusion = False
