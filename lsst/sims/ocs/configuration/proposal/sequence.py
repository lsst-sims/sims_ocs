import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BandFilter
from lsst.sims.ocs.configuration.proposal import Scheduling, SkyConstraints, SkyExclusion, SkyNightlyBounds

__all__ = ["Sequence"]

class Sequence(pexConfig.Config):
    """Configuration for a sequence proposal. This includes sequence, sub-sequence and
       nested sub-sequence proposals.
    """

    name = pexConfig.Field('Name for the proposal.', str)
    sky_user_regions = pexConfig.ListField('Sky user regions for the proposal as a list of field Ids.', int)
    sky_exclusion = pexConfig.ConfigField('Sky region selection for the proposal.', SkyExclusion)
    sky_nightly_bounds = pexConfig.ConfigField('Sky region selection for the proposal.', SkyNightlyBounds)
    sky_constraints = pexConfig.ConfigField('Sky region selection for the proposal.', SkyConstraints)
    filters = pexConfig.ConfigDictField('Filter configuration for the proposal.', str, BandFilter)
    scheduling = pexConfig.ConfigField('Scheduling configuration for the proposal.', Scheduling)

    def setDefaults(self):
        """Default specification for a sequence proposal.
        """
        self.sky_user_regions = []

    def set_topic(self, topic):
        """Set the information on a DDS topic instance.

        Parameters
        ----------
        topic : SALPY_scheduler.scheduler_sequencePropConfigC
            The instance of the DDS topic to set information on.

        Returns
        -------
        SALPY_scheduler.scheduler_sequencePropConfigC
            The topic with current information set.
        """
        topic.name = self.name if self.name is not None else "None"

        topic.twilight_boundary = self.sky_nightly_bounds.twilight_boundary
        topic.delta_lst = self.sky_nightly_bounds.delta_lst
        topic.dec_window = self.sky_exclusion.dec_window
        topic.max_airmass = self.sky_constraints.max_airmass
        topic.max_cloud = self.sky_constraints.max_cloud

        num_sky_user_regions = len(self.sky_user_regions)
        topic.num_user_regions = num_sky_user_regions
        for i, sky_user_region in enumerate(self.sky_user_regions):
            topic.user_region_ids[i] = sky_user_region

        topic.num_filters = len(self.filters) if self.filters is not None else 0
        if topic.num_filters:
            filter_names = []
            exp_index = 0
            for i, v in enumerate(self.filters.values()):
                filter_names.append(v.name)
                topic.bright_limit[i] = v.bright_limit
                topic.dark_limit[i] = v.dark_limit
                topic.max_seeing[i] = v.max_seeing
                topic.num_filter_exposures[i] = len(v.exposures)
                for exposure in v.exposures:
                    topic.exposures[exp_index] = exposure
                    exp_index += 1
            topic.filter_names = ','.join(filter_names)

        topic.max_num_targets = self.scheduling.max_num_targets
        topic.accept_serendipity = self.scheduling.accept_serendipity
        topic.accept_consecutive_visits = self.scheduling.accept_consecutive_visits
        topic.airmass_bonus = self.scheduling.airmass_bonus

        return topic
