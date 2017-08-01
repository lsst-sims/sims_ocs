import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import Scheduling

__all__ = ["SequenceScheduling"]

class SequenceScheduling(Scheduling):
    """Configuration for a Sequence proposal's scheduling needs.
    """

    restart_lost_sequences = pexConfig.Field('Flag to restart sequences that were lost due to '
                                             'observational constraints.', bool)
    restart_complete_sequences = pexConfig.Field('Flag to restart sequences that were already completed.',
                                                 bool)
    max_visits_goal = pexConfig.Field('The maximum number of visits requested for the proposal over the '
                                      'lifetime of the survey. This effects the time-balancing for the '
                                      'proposal, but does not prevent more visits from being taken.', int)

    def setDefaults(self):
        """Default specification for scheduling information.
        """
        Scheduling.setDefaults(self)
        self.max_visits_goal = 250000
        self.restart_lost_sequences = True
        self.restart_complete_sequences = True

    def validate(self):
        """Validate configuration parameters.
        """
        pexConfig.Config.validate(self)
        if self.max_visits_goal < 1:
            raise ValueError("Maximum Visits Goal should be greater than zero.")
