import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import ScienceProposals
from lsst.sims.ocs.kernel.time_handler import BASELINE_SURVEY_DURATION

__all__ = ["Survey"]

class Survey(pexConfig.Config):
    """Configuration for the survey.
    """
    start_date = pexConfig.Field("The start date (format=YYYY-MM-DD) of the survey.", str)
    duration = pexConfig.Field("The fractional duration (units=years) of the survey.", float)
    idle_delay = pexConfig.Field("The delay (units=seconds) to skip the simulation time forward when "
                                 "not receiving a target.", float)
    ad_proposals = pexConfig.ListField("The list of available area distribution proposals.", str)
    alt_proposal_dir = pexConfig.Field("An alternative directory location for proposals.", str, optional=True)

    def setDefaults(self):
        """Set defaults for the survey.
        """
        self.start_date = "2022-01-01"
        self.duration = 1.0
        self.idle_delay = 60.0
        sci_prop = ScienceProposals()
        self.ad_proposals = sci_prop.ad_proposals

    @property
    def full_duration(self):
        """The full duration of the survey.

        Returns
        -------
        double
        """
        if self.duration > BASELINE_SURVEY_DURATION:
            return self.duration
        else:
            return BASELINE_SURVEY_DURATION
