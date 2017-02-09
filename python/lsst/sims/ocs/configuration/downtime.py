import lsst.pex.config as pexConfig

__all__ = ["Downtime"]

class Downtime(pexConfig.Config):
    """Configuration for the scheduled and unscheduled downtime.
    """

    scheduled_downtime_db = pexConfig.Field('Alternate database file for scheduled downtime. Must have same '
                                            'format as internal database.', str)
    unscheduled_downtime_use_random_seed = pexConfig.Field('Use a random seed determining the unscheduled '
                                                           'downtime rather than fixed seed.', bool)
    unscheduled_downtime_random_seed = pexConfig.Field('A placeholder for the random seed used when one is '
                                                       'requested. This is only available in the saved '
                                                       'config.', int)

    def setDefaults(self):
        """Set defaults for the downtime configuration.
        """
        self.scheduled_downtime_db = ""
        self.unscheduled_downtime_use_random_seed = False
        self.unscheduled_downtime_random_seed = -1
