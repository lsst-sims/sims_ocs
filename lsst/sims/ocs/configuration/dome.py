import lsst.pex.config as pexConfig

__all__ = ["Dome"]

class Dome(pexConfig.Config):
    """Configuration of the LSST Dome.
    """

    # Kinematic parameters
    altitude_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of dome altitude movement.',
                                        float)
    altitude_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of dome altitude '
                                     'movement.', float)
    altitude_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of dome altitude '
                                     'movement.', float)

    azimuth_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of dome azimuth movement.',
                                       float)
    azimuth_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of dome azimuth '
                                    'movement.', float)
    azimuth_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of dome azimuth '
                                    'movement.', float)

    settle_time = pexConfig.Field('Times (units=seconds) for the dome to settle after stopping.', float)

    def setDefaults(self):
        """Set defaults for the LSST Dome.
        """
        self.altitude_maxspeed = 1.75
        self.altitude_accel = 0.875
        self.altitude_decel = 0.875
        self.azimuth_maxspeed = 1.5
        self.azimuth_accel = 0.75
        self.azimuth_decel = 0.75
        self.settle_time = 1.0
