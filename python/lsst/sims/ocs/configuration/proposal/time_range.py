import lsst.pex.config as pexConfig

__all__ = ["TimeRange"]

class TimeRange(pexConfig.Config):
    """Configuration for a time range.
    """

    start = pexConfig.Field("The starting time (units=days) for a time-dependent quantity.", int)
    end = pexConfig.Field("The ending time (units=days) for a time-dependent quantity.", int)

    def setDefaults(self):
        """Default specification for a time range.
        """
        self.start = 0
        self.end = 0

    def validate(self):
        """Validate configuration parameters.
        """
        pexConfig.Config.validate(self)
        if self.start > self.end:
            self.start, self.end = self.end, self.start
