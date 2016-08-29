import lsst.pex.config as pexConfig

__all__ = ["SchedulerDriver"]

class SchedulerDriver(pexConfig.Config):
    """Configuration of the LSST Scheduler's Driver.
    """

    coadd_values = pexConfig.Field('Flag to determine if two identical field/filter targets have their '
                                   'ranks added and then considered as one target.', bool)
    time_balancing = pexConfig.Field('Flag to detemine if cross-proposal time-balancing is used.', bool)
    timebonus_tmax = pexConfig.Field("", float)
    timebonus_bmax = pexConfig.Field("", float)
    timebonus_slope = pexConfig.Field("", float)
    night_boundary = pexConfig.Field('Solar altitude (degrees) when it is considered night.', float)

    def setDefaults(self):
        """Set defaults for the LSST Scheduler's Driver.
        """
        self.coadd_values = True
        self.time_balancing = True
        self.timebonus_tmax = 200.0
        self.timebonus_bmax = 10.0
        self.timebonus_slope = 2.26
        self.night_boundary = -12.0
