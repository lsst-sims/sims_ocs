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

    def setDefaults(self):
        """Default specification for scheduling information.
        """
        Scheduling.setDefaults(self)
        self.restart_lost_sequences = True
        self.restart_complete_sequences = True
