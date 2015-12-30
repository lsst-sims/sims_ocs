import math

import lsst.pex.config as pexConfig

__all__ = ["ObservingSite"]

class ObservingSite(pexConfig.Config):
    """Configuration for the observing site.
    """
    name = pexConfig.Field('Telescope site name.', str)
    latitude = pexConfig.Field('Telescope site\'s Latitude (units=degrees), negative implies South.', float)
    longitude = pexConfig.Field('Telescope site\'s Longitude (units=degrees), negative implies West', float)
    height = pexConfig.Field('Telescope site\'s Elevation (units=meters above sea level)', float)
    pressure = pexConfig.Field('Telescope site\'s atmospheric pressure (units=millibars)', float)
    temperature = pexConfig.Field('Telescope site\'s atmospheric temperature (units=degrees C)', float)
    relativeHumidity = pexConfig.Field('Telescope site\'s relative humidity (units=percent)', float)

    def setDefaults(self):
        """Set defaults for the Cerro Pachon observing site.
        """
        self.name = "Cerro Pachon"
        self.latitude = -30.2444  # OSS-REQ-0008 (LSE-30)
        self.longitude = -70.7494  # OSS-REQ-0008 (LSE-30)
        self.height = 2650.  # OSS-REQ-0008 (LSE-30)
        self.pressure = 1010.0
        self.temperature = 12.0
        self.relativeHumidity = 0.0

    @property
    def latitude_rads(self):
        """float: The observing site latitude in radians.
        """
        return math.radians(self.latitude)

    @property
    def longitude_rads(self):
        """float: The observing site longitude in radians.
        """
        return math.radians(self.longitude)
