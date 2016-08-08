import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BandFilter, Scheduling
from lsst.sims.ocs.configuration.proposal import SkyConstraints, SkyExclusion, SkyNightlyBounds, SkyRegion

__all__ = ["AreaDistribution"]

class AreaDistribution(pexConfig.Config):
    """Configuration for an area distribution proposal.
    """

    name = pexConfig.Field('Name for the proposal.', str)
    sky_region = pexConfig.ConfigField('Sky region selectionfor the proposal.', SkyRegion)
    sky_exclusion = pexConfig.ConfigField('Sky region selectionfor the proposal.', SkyExclusion)
    sky_nightly_bounds = pexConfig.ConfigField('Sky region selectionfor the proposal.', SkyNightlyBounds)
    sky_constraints = pexConfig.ConfigField('Sky region selectionfor the proposal.', SkyConstraints)
    filters = pexConfig.ConfigDictField('Filter configuration for the proposal.', str, BandFilter)
    scheduling = pexConfig.ConfigField('Scheduling configuration for the proposal.', Scheduling)

    def set_topic(self, topic):
        """Set the information on a DDS topic instance.

        Parameters
        ----------
        topic : SALPY_scheduler.scheduler_areaDistPropConfigC
            The instance of the DDS topic to set information on.

        Returns
        -------
        SALPY_scheduler.scheduler_areaDistPropConfigC
            The topic with current information set.
        """
        topic.name = self.name if self.name is not None else "None"

        topic.twilight_boundary = self.sky_nightly_bounds.twilight_boundary
        topic.delta_lst = self.sky_nightly_bounds.delta_lst
        topic.dec_window = self.sky_exclusion.dec_window

        num_region_selections = len(self.sky_region.selections) \
            if self.sky_region.selections is not None else 0
        topic.num_region_selections = num_region_selections
        if num_region_selections:
            limit_types = []
            for i, v in enumerate(self.sky_region.selections.values()):
                limit_types.append(v.limit_type)
                topic.region_minimums[i] = v.minimum_limit
                topic.region_maximums[i] = v.maximum_limit
                topic.region_bounds[i] = v.bounds_limit
            topic.region_types = ','.join(limit_types)

        topic.region_combiners = ','.join(self.sky_region.combiners)

        num_exclusion_selections = len(self.sky_exclusion.selections) \
            if self.sky_exclusion.selections is not None else 0
        topic.num_exclusion_selections = num_exclusion_selections
        if num_exclusion_selections:
            limit_types = []
            for i, v in enumerate(self.sky_exclusion.selections.values()):
                limit_types.append(v.limit_type)
                topic.exclusion_minimums[i] = v.minimum_limit
                topic.exclusion_maximums[i] = v.maximum_limit
                topic.exclusion_bounds[i] = v.bounds_limit
            topic.exclusion_types = ','.join(limit_types)

        topic.num_filters = len(self.filters) if self.filters is not None else 0
        if topic.num_filters:
            filter_names = []
            exp_index = 0
            for i, v in enumerate(self.filters.values()):
                filter_names.append(v.name)
                topic.num_visits[i] = v.num_visits
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

        return topic
