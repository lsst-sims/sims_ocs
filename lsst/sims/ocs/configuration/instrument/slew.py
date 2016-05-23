import lsst.pex.config as pexConfig

__all__ = ["Slew"]

class Slew(pexConfig.Config):
    """Configuration of the LSST Slew.
    """

    tel_optics_ol_slope = pexConfig.Field('Delay factor for Open Loop optics correction '
                                          '(units=seconds/(degrees in ALT slew)', float)

    # Table of delay factors for Closed Loop optics correction according to the ALT slew range.
    tel_optics_cl_alt_limit = pexConfig.ListField('Altitude (units=degrees) limits for the delay ranges.',
                                                  float)

    tel_optics_cl_delay = pexConfig.ListField('Time delay (units=seconds) for the corresponding ALT slew '
                                              'range in the Closed Loop optics correction.', float)

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
        self.tel_optics_ol_slope = 1.0 / 3.5
        self.tel_optics_cl_alt_limit = [0.0, 9.0, 90.0]
        self.tel_optics_cl_delay = [0.0, 20.0]

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

    def set_array(self, conf, param):
        """Set a DDS topic array parameter.

        Parameters
        ----------
        conf : SALPY_scheduler.scheduler_slewConfigC
            The slew configuration instance.
        param : str
            The name of the topic parameter to fill.
        """
        array = getattr(conf, param)
        local_param = getattr(self, param)
        for i, v in enumerate(local_param):
            array[i] = v

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
