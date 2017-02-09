import lsst.pex.config as pexConfig

__all__ = ["Slew"]

class Slew(pexConfig.Config):
    """Configuration of the LSST Slew.
    """

    # Dependencies between the slew activities.
    # For each activity there is a list of prerequisites activities, that must be previously completed.
    # The Readout corresponds to the previous observation, that's why it doesn't have prerequisites and it is
    # a prerequisite for Exposure.
    prereq_domalt = pexConfig.ListField('Prerequisite list for dome altitude movement.', str)
    prereq_domaz = pexConfig.ListField('Prerequisite list for dome azimuth movement.', str)
    prereq_telalt = pexConfig.ListField('Prerequisite list for telescope altitude movement.', str)
    prereq_telaz = pexConfig.ListField('Prerequisite list for telescope azimuth movement.', str)
    prereq_telopticsopenloop = pexConfig.ListField('Prerequisite list for telescope optics open loop '
                                                   'corrections.', str)
    prereq_telopticsclosedloop = pexConfig.ListField('Prerequisite list for telescope optics closed loop '
                                                     'corrections.', str)
    prereq_telrot = pexConfig.ListField('Prerequisite list for telescope rotator movement.', str)
    prereq_filter = pexConfig.ListField('Prerequisite list for filter movement.', str)
    prereq_adc = pexConfig.ListField('Prerequisite list for the ADC', str)
    prereq_ins_optics = pexConfig.ListField('Prerequisite list for instrument optics.', str)
    prereq_guider_pos = pexConfig.ListField('Prerequisite list for the guider positioning.', str)
    prereq_guider_adq = pexConfig.ListField('Prerequisite list for the guider adq?', str)
    prereq_telsettle = pexConfig.ListField('Prerequisite list for telescope settle time.', str)
    prereq_domazsettle = pexConfig.ListField('Prerequisite list for the dome settle time.', str)
    prereq_exposures = pexConfig.ListField('Prerequisite list for exposure time.', str)
    prereq_readout = pexConfig.ListField('Prerequisite list for camera electronics readout time.', str)

    def setDefaults(self):
        """Set defaults for the LSST Slew.
        """

        self.prereq_domalt = []
        self.prereq_domaz = []
        self.prereq_domazsettle = ['domaz']
        self.prereq_telalt = []
        self.prereq_telaz = []
        self.prereq_telrot = []
        self.prereq_telopticsopenloop = ['telalt', 'telaz']
        self.prereq_telopticsclosedloop = ['domalt', 'domazsettle', 'telsettle', 'readout',
                                           'telopticsopenloop', 'filter', 'telrot']
        self.prereq_telsettle = ['telalt', 'telaz']
        self.prereq_filter = []
        self.prereq_exposures = ['telopticsclosedloop']
        self.prereq_readout = []
        self.prereq_adc = []
        self.prereq_ins_optics = []
        self.prereq_guider_pos = []
        self.prereq_guider_adq = []

    def get_string_rep(self, param):
        """A string representation of a string list parameter.

        Parameters
        ----------
        param : str
            The string list parameter name.

        Returns
        -------
        str
        """
        local_param = getattr(self, param)
        return ",".join(local_param)
