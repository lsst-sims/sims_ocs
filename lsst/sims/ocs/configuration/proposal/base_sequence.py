import lsst.pex.config as pexConfig

__all__ = ["BaseSequence"]

class BaseSequence(pexConfig.Config):
    """Part of the configuration for sub-sequences.
    """

    num_events = pexConfig.Field('The number of required events for the sub-sequence.', int)
    num_max_missed = pexConfig.Field('The maximum number of events the sub-sequence is allowed to miss.', int)
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

    def setDefaults(self):
        """Default specification for BaseSequence information.
        """
        self.num_events = 0
        self.num_max_missed = 0
        self.time_interval = 0.0
        self.time_window_start = 0.0
        self.time_window_max = 0.0
        self.time_window_end = 0.0
        self.time_weight = 0.0
