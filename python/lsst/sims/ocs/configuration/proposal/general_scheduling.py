import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import Scheduling

__all__ = ["GeneralScheduling"]

class GeneralScheduling(Scheduling):
    """Configuration for a general proposal's scheduling needs.
    """

    restrict_grouped_visits = pexConfig.Field('Flag to restrict the number of grouped visits per night to '
                                              'the requested number.', bool)
    time_interval = pexConfig.Field('Time (units=seconds) between subsequent visits for a field/filter '
                                    'combination. Must be non-zero if number of grouped visits is greater '
                                    'than one.', float)
    time_window_start = pexConfig.Field('Relative time when the window opens for subsequent grouped visits.',
                                        float)
    time_window_max = pexConfig.Field('Relative time when the window reaches maximum rank for subsequent '
                                      'grouped visits.', float)
    time_window_end = pexConfig.Field('Relative time when the window ends for subsequent grouped visits.',
                                      float)
    time_weight = pexConfig.Field('Weighting factor for scaling the shape of the time window.', float)
    field_revisit_limit = pexConfig.Field('Maximum number of revisits a field may get for the night', int)

    def setDefaults(self):
        """Default specification for scheduling information.
        """
        Scheduling.setDefaults(self)
        self.restrict_grouped_visits = True
        self.time_interval = 0.0
        self.time_window_start = 0.0
        self.time_window_max = 0.0
        self.time_window_end = 0.0
        self.time_weight = 0.0
        self.field_revisit_limit = 0
