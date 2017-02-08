import lsst.pex.config as pexConfig

__all__ = ["Park"]

class Park(pexConfig.Config):
    """Configuration of the LSST Observatory Park position.
    """

    telescope_altitude = pexConfig.Field("Telescope altitude (units=degrees) in the park position.", float)
    telescope_azimuth = pexConfig.Field("Telescope azimuth (units=degrees) in the park position.", float)
    telescope_rotator = pexConfig.Field("Telescope rotator angle (units=degrees) in the park position.",
                                        float)
    dome_altitude = pexConfig.Field("Dome altitude (units=degrees) in the park position.", float)
    dome_azimuth = pexConfig.Field("Dome azimuth (units=degrees) in the park position.", float)
    filter_position = pexConfig.Field("Camera filter for the park position.", str)

    def setDefaults(self):
        """Set defaults for the LSST Observatory Park position.
        """
        self.telescope_altitude = 86.5
        self.telescope_azimuth = 0.0
        self.telescope_rotator = 0.0
        self.dome_altitude = 90.0
        self.dome_azimuth = 0.0
        self.filter_position = 'r'
