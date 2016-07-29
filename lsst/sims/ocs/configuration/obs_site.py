import math

import lsst.pex.config as pexConfig
import lsst.sims.utils as simsUtils

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
    relative_humidity = pexConfig.Field('Telescope site\'s relative humidity (units=percent)', float)

    def setDefaults(self):
        """Set defaults for the Cerro Pachon observing site.
        """
        lsst = simsUtils.Site(name="LSST")
        self.name = "Cerro Pachon"
        self.latitude = lsst.latitude
        self.longitude = lsst.longitude
        self.height = lsst.height
        self.pressure = lsst.pressure
        self.temperature = lsst.temperature
        self.relative_humidity = lsst.humidity

    @property
    def latitude_rad(self):
        """float: The observing site latitude in radians.
        """
        return math.radians(self.latitude)

    @property
    def longitude_rad(self):
        """float: The observing site longitude in radians.
        """
        return math.radians(self.longitude)
