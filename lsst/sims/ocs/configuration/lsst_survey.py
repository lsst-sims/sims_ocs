import lsst.pex.config as pexConfig

__all__ = ["LsstSurvey"]

class LsstSurvey(pexConfig.Config):
    """Configuration for the LSST Survey.
    """
    start_date = pexConfig.Field("The start date of the LSST Survey. Format is YYYY-MM-DD.", str)
    duration = pexConfig.Field("The fractional duration in years of the survey.", float)

    def setDefaults(self):
        """Set the defaults for the LSST Survey.

        This function sets the default parameters for the LSST Survey.
        """
        self.start_date = "2020-05-24"
        self.duration = 1.0
