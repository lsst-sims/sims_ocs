import lsst.pex.config as pexConfig

__all__ = ["Telescope"]

class Telescope(pexConfig.Config):
    """Configuration of the LSST Telescope.
    """

    # Altitude limits
    alt_min = pexConfig.Field('The minimum altitude of the telescope from horizon (units=degrees)', float)
    alt_max = pexConfig.Field('The maximum altitude of the telescope for zenith avoidance (units=degrees)',
                              float)

    # Absolute position limits due to cable wrap the range [0 360] must be included
    az_minpos = pexConfig.Field('Minimum absolute azimuth limit (units=degrees) of telescope.', float)
    az_maxpos = pexConfig.Field('Maximum absolute azimuth limit (units=degrees) of telescope.', float)

    # Kinematic parameters
    alt_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of telescope altitude movement.',
                                   float)
    alt_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of telescope altitude '
                                'movement.', float)
    alt_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of telescope altitude '
                                'movement.', float)

    az_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of telescope azimuth movement.',
                                  float)
    az_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of telescope azimuth '
                               'movement.', float)
    az_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of telescope azimuth '
                               'movement.', float)

    settle_time = pexConfig.Field('Time (units=seconds) for the telescope mount to settle after stopping.',
                                  float)

    def setDefaults(self):
        """Set defaults for the LSST Telescope.
        """
        self.alt_min = 20.0
        self.alt_max = 86.5
        self.az_minpos = -270.0
        self.az_maxpos = 270.0
        self.alt_maxspeed = 3.5
        self.alt_accel = 3.5
        self.alt_decel = 3.5
        self.az_maxspeed = 7.0
        self.az_accel = 7.0
        self.az_decel = 7.0
        self.settle_time = 3.0
