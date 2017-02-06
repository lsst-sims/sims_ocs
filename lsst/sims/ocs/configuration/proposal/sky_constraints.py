import lsst.pex.config as pexConfig

__all__ = ["SkyConstraints"]

class SkyConstraints(pexConfig.Config):
    """Configuration for a proposal's sky constraints.
    """

    max_airmass = pexConfig.Field('The maximum airmass allowed for any field.', float)
    max_cloud = pexConfig.Field('The maximum fraction of clouds allowed for any field.', float)
    min_distance_moon = pexConfig.Field('The minimum distance (units=degrees) from the moon a field must be.',
                                        float)
    exclude_planets = pexConfig.Field('Flag to use 2 degree exclusion zone around bright planets.', bool)

    def setDefaults(self):
        """Default specification for sky constarints.
        """
        self.max_airmass = 2.5
        self.max_cloud = 0.7
        self.min_distance_moon = 30.0
        self.exclude_planets = True
