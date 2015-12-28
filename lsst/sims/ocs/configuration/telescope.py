import lsst.pex.config as pexConfig

__all__ = ["Telescope"]

class Telescope(pexConfig.Config):
    """Configuration of the LSST Telescope.
    """

    # Altitude limits
    altitude_min = pexConfig.Field('The minimum altitude of the telescope from horizon (units=degrees)',
                                   float)
    altitude_max = pexConfig.Field('The maximum altitude of the telescope for zenith avoidance '
                                   '(units=degrees)', float)

    # Absolute position limits due to cable wrap the range [0 360] must be included
    azimuth_minpos = pexConfig.Field('Minimum absolute azimuth limit (units=degrees) of telescope.', float)
    azimuth_maxpos = pexConfig.Field('Maximum absolute azimuth limit (units=degrees) of telescope.', float)

    # Kinematic parameters
    altitude_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of telescope altitude '
                                        'movement.', float)
    altitude_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of telescope altitude '
                                     'movement.', float)
    altitude_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of telescope altitude '
                                     'movement.', float)

    azimuth_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of telescope azimuth movement.',
                                       float)
    azimuth_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of telescope azimuth '
                                    'movement.', float)
    azimuth_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of telescope azimuth '
                                    'movement.', float)

    settle_time = pexConfig.Field('Time (units=seconds) for the telescope mount to settle after stopping.',
                                  float)

    def setDefaults(self):
        """Set defaults for the LSST Telescope.
        """
        self.altitude_min = 20.0
        self.altitude_max = 86.5
        self.azimuth_minpos = -270.0
        self.azimuth_maxpos = 270.0
        self.altitude_maxspeed = 3.5
        self.altitude_accel = 3.5
        self.altitude_decel = 3.5
        self.azimuth_maxspeed = 7.0
        self.azimuth_accel = 7.0
        self.azimuth_decel = 7.0
        self.settle_time = 3.0
