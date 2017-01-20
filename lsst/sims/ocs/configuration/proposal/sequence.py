import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BandFilter, MasterSubSequence, Scheduling, SkyConstraints
from lsst.sims.ocs.configuration.proposal import SkyExclusion, SkyNightlyBounds, SubSequence

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
    sub_sequences = pexConfig.ConfigDictField('Set of sub-sequences.', int, SubSequence)
    master_sub_sequences = pexConfig.ConfigDictField('Set of master sub-sequences.', int, MasterSubSequence)
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

        num_sub_sequences = len(self.sub_sequences) if self.sub_sequences is not None else 0
        topic.num_sub_sequences = num_sub_sequences
        if topic.num_sub_sequences:
            sub_sequence_names = []
            sub_sequence_filters = []
            filter_visit_index = 0
            for i, sub_sequence in self.sub_sequences.items():
                sub_sequence_names.append(sub_sequence.name)
                sub_sequence_filters.append(sub_sequence.get_filter_string())
                topic.num_sub_sequence_filters[i] = len(sub_sequence.filters)
                for filter_visit in sub_sequence.visits_per_filter:
                    topic.num_sub_sequence_filter_visits[filter_visit_index] = filter_visit
                    filter_visit_index += 1
                topic.num_sub_sequence_events[i] = sub_sequence.num_events
                topic.num_sub_sequence_max_missed[i] = sub_sequence.num_max_missed
                topic.sub_sequence_time_intervals[i] = sub_sequence.time_interval
                topic.sub_sequence_time_window_starts[i] = sub_sequence.time_window_start
                topic.sub_sequence_time_window_maximums[i] = sub_sequence.time_window_max
                topic.sub_sequence_time_window_ends[i] = sub_sequence.time_window_end
                topic.sub_sequence_time_weights[i] = sub_sequence.time_weight

            topic.sub_sequence_names = ",".join(sub_sequence_names)
            topic.sub_sequence_filters = ",".join(sub_sequence_filters)

        num_master_sub_sequences = len(self.master_sub_sequences) \
            if self.master_sub_sequences is not None else 0
        topic.num_master_sub_sequences = num_master_sub_sequences
        if topic.num_master_sub_sequences:
            master_sub_sequence_names = []
            nested_sub_sequence_names = []
            for i, master_sub_sequence in self.master_sub_sequences.items():
                master_sub_sequence_names.append(master_sub_sequence.name)
                topic.num_nested_sub_sequences[i] = len(master_sub_sequence.sub_sequences)
                topic.num_master_sub_sequence_events[i] = master_sub_sequence.num_events
                topic.num_master_sub_sequence_max_missed[i] = master_sub_sequence.num_max_missed
                topic.master_sub_sequence_time_intervals[i] = master_sub_sequence.time_interval
                topic.master_sub_sequence_time_window_starts[i] = master_sub_sequence.time_window_start
                topic.master_sub_sequence_time_window_maximums[i] = master_sub_sequence.time_window_max
                topic.master_sub_sequence_time_window_ends[i] = master_sub_sequence.time_window_end
                topic.master_sub_sequence_time_weights[i] = master_sub_sequence.time_weight

            topic.master_sub_sequence_names = ",".join(master_sub_sequence_names)
            topic.nested_sub_sequence_names = ",".join(nested_sub_sequence_names)

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
