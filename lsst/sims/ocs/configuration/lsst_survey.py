import collections
import importlib

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import area_dist_prop_reg, load_class
from lsst.sims.ocs.configuration.proposal import AreaDistribution

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

    def load_proposals(self):
        """Load proposals from configuration.science module.
        """

        AREA_DIST = "AreaDistribution"
        proposal_dict = collections.defaultdict(list)

        proposal_module = "lsst.sims.ocs.configuration.science"
        module = importlib.import_module(proposal_module)
        names = dir(module)
        for name in names:
            cls = load_class(proposal_module + "." + name)
            try:
                key = None
                if issubclass(cls, AreaDistribution):
                    key = AREA_DIST
                if key is not None:
                    proposal_dict[key].append(cls.__name__)
            except TypeError:
                # Don't care about things that aren't classes.
                pass

        self.area_dist_props.names = proposal_dict[AREA_DIST]
