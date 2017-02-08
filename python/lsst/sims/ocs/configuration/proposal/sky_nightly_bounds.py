import lsst.pex.config as pexConfig

__all__ = ["SkyNightlyBounds"]

class SkyNightlyBounds(pexConfig.Config):
    """Configuration for a proposal's nightly sky bounds.
    """

    twilight_boundary = pexConfig.Field('The sun altitude (units=degrees) for twilight consideration.', float)

    delta_lst = pexConfig.Field('LST extent (units=degrees) before sunset LST (-) and after sunrise LST (+) '
                                'for providing a region of the sky to select.', float)

    def setDefaults(self):
        """Default specification for nightly sky bounds.
        """

        self.twilight_boundary = -12.0
        self.delta_lst = 30.0
