import lsst.pex.config as pexConfig

__all__ = ["Scheduling"]

class Scheduling(pexConfig.Config):
    """Configuration for a proposal's scheduling needs.
    """

    max_num_targets = pexConfig.Field('The maximum number of targets the proposal will propose.', int)
    accept_serendipity = pexConfig.Field('Flag to determine if observations other than proposal\'s top '
                                         'target are accepted.', bool)
    accept_consecutive_visits = pexConfig.Field('Flag to determine if consecutive visits are accepted.', bool)
    airmass_bonus = pexConfig.Field('Bonus to apply to fields giving precidence to low arimass ones. '
                                    'Bonus runs from 0 to 1.', float)
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

    def setDefaults(self):
        """Default specification for scheduling information.
        """

        self.max_num_targets = 100
        self.accept_serendipity = True
        self.accept_consecutive_visits = True
        self.airmass_bonus = 0.5
        self.restrict_grouped_visits = True
        self.time_interval = 0.0
        self.time_window_start = 0.0
        self.time_window_max = 0.0
        self.time_window_end = 0.0
        self.time_weight = 0.0
