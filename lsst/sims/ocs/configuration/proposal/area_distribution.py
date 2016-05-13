import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BandFilter, Scheduling, SkyRegion

__all__ = ["AreaDistribution"]

class AreaDistribution(pexConfig.Config):
    """Configuration for an area distribution proposal.
    """

    name = pexConfig.Field('Name for the proposal.', str)
    sky_region = pexConfig.ConfigField('Sky selection region for the proposal.', SkyRegion)
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

        topic.twilight_boundary = self.sky_region.twilight_boundary
        topic.delta_lst = self.sky_region.delta_lst
        topic.dec_window = self.sky_region.dec_window

        num_limit_selections = len(self.sky_region.limit_selections) \
            if self.sky_region.limit_selections is not None else 0
        topic.num_limit_selections = num_limit_selections
        if num_limit_selections:
            limit_types = []
            for i, v in enumerate(self.sky_region.limit_selections.values()):
                limit_types.append(v.limit_type)
                topic.limit_minimums[i] = v.minimum_limit
                topic.limit_maximums[i] = v.maximum_limit
            topic.limit_types = ','.join(limit_types)

        topic.use_galactic_exclusion = self.sky_region.use_galactic_exclusion
        topic.taper_l = self.sky_region.galactic_exclusion.taper_l
        topic.taper_b = self.sky_region.galactic_exclusion.taper_b
        topic.peak_l = self.sky_region.galactic_exclusion.peak_l

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
            topic.filter_name = ','.join(filter_names)

        topic.max_num_targets = self.scheduling.max_num_targets
        topic.accept_serendipity = self.scheduling.accept_serendipity
        topic.accept_consecutive_visits = self.scheduling.accept_consecutive_visits

        return topic
