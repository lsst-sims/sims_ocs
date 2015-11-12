import lsst.pex.config as pexConfig

__all__ = ["LsstSurvey"]

class LsstSurvey(pexConfig.Config):
    """Configuration for the LSST Survey.
    """
    start_date = pexConfig.Field("The start date (format=YYYY-MM-DD) of the LSST Survey.", str)
    duration = pexConfig.Field("The fractional duration (units=years) of the survey.", float)

    def setDefaults(self):
        """Set defaults for the LSST Survey.
        """
        self.start_date = "2020-05-24"
        self.duration = 1.0
