import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import area_dist_prop_reg

__all__ = ["LsstSurvey"]

class LsstSurvey(pexConfig.Config):
    """Configuration for the LSST Survey.
    """
    start_date = pexConfig.Field("The start date (format=YYYY-MM-DD) of the LSST Survey.", str)
    duration = pexConfig.Field("The fractional duration (units=years) of the survey.", float)
    area_dist_props = area_dist_prop_reg.makeField('The list of area distribution proposals.', multi=True)

    def setDefaults(self):
        """Set defaults for the LSST Survey.
        """
        self.start_date = "2022-01-01"
        self.duration = 1.0
