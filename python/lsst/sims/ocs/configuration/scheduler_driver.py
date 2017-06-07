import lsst.pex.config as pexConfig

__all__ = ["SchedulerDriver"]

class SchedulerDriver(pexConfig.Config):
    """Configuration of the LSST Scheduler's Driver.
    """

    coadd_values = pexConfig.Field('Flag to determine if two identical field/filter targets have their '
                                   'ranks added and then considered as one target.', bool)
    time_balancing = pexConfig.Field('Flag to detemine if cross-proposal time-balancing is used.', bool)
    timecost_time_max = pexConfig.Field('The slew time (units=seconds) where the time cost value equals '
                                        'one.', float)
    timecost_time_ref = pexConfig.Field('The reference slew time (units=seconds) that sets the steepness of '
                                        'the cost function.', float)
    timecost_cost_ref = pexConfig.Field('The cost value associated with the time cost reference slew time.',
                                        float)
    timecost_weight = pexConfig.Field('The weighting value to apply to the slew time cost function result.',
                                      float)
    filtercost_weight = pexConfig.Field('The weighting value to apply to the filter change cost function '
                                        'result.', float)
    night_boundary = pexConfig.Field('Solar altitude (degrees) when it is considered night.', float)
    new_moon_phase_threshold = pexConfig.Field('New moon phase threshold for swapping to dark time filter.',
                                               float)
    ignore_sky_brightness = pexConfig.Field('Flag to ignore sky brightness limits when rejecting targets.',
                                            bool)
    ignore_airmass = pexConfig.Field('Flag to ignore airmass limits when rejecting targets.', bool)
    ignore_clouds = pexConfig.Field('Flag to ignore cloud limits when rejecting targets.', bool)
    ignore_seeing = pexConfig.Field('Flag to ignore seeing limits when rejecting targets.', bool)

    def setDefaults(self):
        """Set defaults for the LSST Scheduler's Driver.
        """
        self.coadd_values = True
        self.time_balancing = True
        self.timecost_time_max = 150.0
        self.timecost_time_ref = 5.0
        self.timecost_cost_ref = 0.3
        self.timecost_weight = 1.0
        self.filtercost_weight = 1.0
        self.night_boundary = -12.0
        self.new_moon_phase_threshold = 20.0
        self.ignore_sky_brightness = False
        self.ignore_airmass = False
        self.ignore_clouds = False
        self.ignore_seeing = False
