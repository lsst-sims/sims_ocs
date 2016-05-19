import lsst.pex.config as pexConfig

__all__ = ["Survey"]

class Survey(pexConfig.Config):
    """Configuration for the survey.
    """
    start_date = pexConfig.Field("The start date (format=YYYY-MM-DD) of the survey.", str)
    duration = pexConfig.Field("The fractional duration (units=years) of the survey.", float)
    idle_delay = pexConfig.Field("The delay (units=seconds) to skip the simulation time forward when"
                                 "not receiving a target.", float)

    def setDefaults(self):
        """Set defaults for the survey.
        """
        self.start_date = "2022-01-01"
        self.duration = 1.0
        self.idle_delay = 60.0
