import lsst.pex.config as pexConfig

__all__ = ["Scheduling"]

class Scheduling(pexConfig.Config):
    """Configuration for a proposal's scheduling needs.
    """

    max_num_targets = pexConfig.Field('The maximum number of targets the proposal will propose.', int)
    accept_serendipity = pexConfig.Field('Flag to determine if observations other than proposal\'s top '
                                         'target are accepted.', bool)
    accept_consecutive_visits = pexConfig.Field('Flag to determine if consecutive visits are accepted.', bool)
    airmass_bonus = pexConfig.Field('Bonus to apply to fields giving precedence to low arimass ones. '
                                    'Bonus runs from 0 to 1.', float)
    hour_angle_bonus = pexConfig.Field('Bonus to apply to fields giving precedence to fields near the '
                                       'meridian. Bonus runs from 0 to 1.', float)

    def setDefaults(self):
        """Default specification for scheduling information.
        """

        self.max_num_targets = 100
        self.accept_serendipity = True
        self.accept_consecutive_visits = True
        self.airmass_bonus = 0.5
        self.hour_angle_bonus = 0.0
