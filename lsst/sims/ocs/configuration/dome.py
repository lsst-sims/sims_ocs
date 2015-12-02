import lsst.pex.config as pexConfig

__all__ = ["Dome"]

class Dome(pexConfig.Config):
    """Configuration of the LSST Dome.
    """

    # Kinematic parameters
    alt_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of dome altitude movement.', float)
    alt_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of dome altitude movement.',
                                float)
    alt_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of dome altitude movement.',
                                float)

    az_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of dome azimuth movement.', float)
    az_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of dome azimuth movement.',
                               float)
    az_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of dome azimuth movement.',
                               float)

    settle_time = pexConfig.Field('Times (units=seconds) for the dome to settle after stopping.', float)

    def setDefaults(self):
        """Set defaults for the LSST Dome.
        """
        self.alt_maxspeed = 1.75
        self.alt_accel = 0.875
        self.alt_decel = 0.875
        self.az_maxspeed = 1.5
        self.az_accel = 0.75
        self.az_decel = 0.75
        self.settle_time = 1.0
