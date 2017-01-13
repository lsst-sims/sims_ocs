import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import Scheduling, SkyConstraints, SkyNightlyBounds

__all__ = ["Sequence"]

class Sequence(pexConfig.Config):
    """Configuration for a sequence proposal. This includes sequence, sub-sequence and
       nested sub-sequence proposals.
    """

    name = pexConfig.Field('Name for the proposal.', str)
    sky_user_regions = pexConfig.ListField('Sky user regions for the proposal as a list of field Ids.', int)
    sky_nightly_bounds = pexConfig.ConfigField('Sky region selection for the proposal.', SkyNightlyBounds)
    sky_constraints = pexConfig.ConfigField('Sky region selection for the proposal.', SkyConstraints)
    scheduling = pexConfig.ConfigField('Scheduling configuration for the proposal.', Scheduling)

    def setDefaults(self):
        """Default specification for a sequence proposal.
        """
        self.sky_user_regions = []
