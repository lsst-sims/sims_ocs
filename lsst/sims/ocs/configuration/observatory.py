import lsst.pex.config as pexConfig

__all__ = ["Observatory"]

class Observatory(pexConfig.Config):
    """Configuration of the LSST observatory.
    """
    # Telescope altitude limits
    tel_alt_min = pexConfig.Field('The minimum altitude of the telescope from horizon (units=degrees)', float)
    tel_alt_max = pexConfig.Field('The maximum altitude of the telescope for zenith avoidance '
                                  '(units=degrees)', float)

    # Absolute position limits due to cable wrap the range [0 360] must be included
    tel_az_minpos = pexConfig.Field('Minimum absolute azimuth limit (units=degrees) of telescope.', float)
    tel_az_maxpos = pexConfig.Field('Maximum absolute azimuth limit (units=degrees) of telescope.', float)

    # Telescope kinematic parameters
    tel_alt_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of telescope altitude movement.',
                                       float)
    tel_alt_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of telescope altitude '
                                    'movement.', float)
    tel_alt_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of telescope altitude '
                                    'movement.', float)

    tel_az_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of telescope azimuth movement.',
                                      float)
    tel_az_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of telescope azimuth '
                                   'movement.', float)
    tel_az_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of telescope azimuth '
                                   'movement.', float)

    # Dome kinematic parameters
    dom_alt_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of dome altitude movement.',
                                       float)
    dom_alt_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of dome altitude '
                                    'movement.', float)
    dom_alt_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of dome altitude '
                                    'movement.', float)

    dom_az_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of dome azimuth movement.', float)
    dom_az_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of dome azimuth '
                                   'movement.', float)
    dom_az_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of dome azimuth '
                                   'movement.', float)

    # Rotator parameters
    rotator_minpos = pexConfig.Field('Minimum position (units=degrees) of rotator.', float)
    rotator_maxpos = pexConfig.Field('Maximum position (units=degrees) of rotator.', float)

    rotator_followsky = pexConfig.Field('Flag that if True enables the movement of the rotator during slews '
                                        'to put North-Up. If range is insufficient, then the alignment is '
                                        'North-Down. If the flag is False, then the rotator does not move '
                                        'during the slews, it is only tracking during the exposures.', bool)
    rotator_resume_angle_after_filter_change = pexConfig.Field('Flag that if True enables the rotator to '
                                                               'keep the image angle after a filter change, '
                                                               'moving back the rotator to the previous '
                                                               'angle after the rotator was placed in filter '
                                                               'change position. If the flag is False, then '
                                                               'the rotator is left in the filter change '
                                                               'position.', bool)

    # Rotator kinemtatic parameters
    rotator_maxspeed = pexConfig.Field('Maximum speed (units=degrees/second) of rotator movement.', float)
    rotator_accel = pexConfig.Field('Maximum acceleration (units=degrees/second**2) of rotator movement.',
                                    float)
    rotator_decel = pexConfig.Field('Maximum deceleration (units=degrees/second**2) of rotator movement.',
                                    float)

    # Slew time parameters
    filter_mounttime = pexConfig.Field('Time (units=seconds) to mount a filter.', float)
    filter_movetime = pexConfig.Field('Time (units=seconds) to move a filter.', float)

    tel_settle_time = pexConfig.Field('Time (units=seconds) for the telescope mount to settle after '
                                      'stopping.', float)

    dome_settle_time = pexConfig.Field('Times (units=seconds) for the dome to settle after stopping.', float)

    camera_readout_time = pexConfig.Field('Time (units=seconds) for the camera electronics readout.', float)
    camera_shutter_time = pexConfig.Field('Time (units=seconds) for the camera shutter to open or close',
                                          float)

    tel_optics_ol_slope = pexConfig.Field('Delay factor for Open Loop optics correction '
                                          '(units=seconds/(degrees in ALT slew)', float)

    # Table of delay factors for Closed Loop optics correction according to the ALT slew range.
    tel_optics_alt_limit = pexConfig.ListField('Altitude (units=degrees) limits for the delay ranges.', float)

    tel_optics_cl_delay = pexConfig.ListField('Time delay (units=seconds) for the corresponding ALT slew '
                                              'range in the Closed Loop optics correction.', float)

    # Camera filter parameters
    filter_mounted = pexConfig.ListField('Initial state for the mounted filters. Empty positions must be '
                                         'filled with id="" no (filter).', str)
    filter_pos = pexConfig.Field('The currently mounted filter.', str)
    filter_removable = pexConfig.ListField('The list of filters that can be removed.', str)
    filter_unmounted = pexConfig.ListField('The list of unmounted but available to swap filters.', str)

    # Dependencies between the slew activities.
    # For each activity there is a list of prerequisites activities, that must be previously completed.
    # The Readout corresponds to the previous observation, that's why it doesn't have prerequisites and it is
    # a prerequisite for Exposure.
    prereq_dom_alt = pexConfig.ListField('Prerequisite list for dome altitude movement.', str)
    prereq_dom_az = pexConfig.ListField('Prerequisite list for dome azimuth movement.', str)
    prereq_tel_alt = pexConfig.ListField('Prerequisite list for telescope altitude movement.', str)
    prereq_tel_az = pexConfig.ListField('Prerequisite list for telescope azimuth movement.', str)
    prereq_tel_optics_ol = pexConfig.ListField('Prerequisite list for telescope optics open loop '
                                               'corrections.', str)
    prereq_tel_optics_cl = pexConfig.ListField('Prerequisite list for telescope optics closed loop '
                                               'corrections.', str)
    prereq_rotator = pexConfig.ListField('Prerequisite list for rotator movement.', str)
    prereq_filter = pexConfig.ListField('Prerequisite list for filter movement.', str)
    prereq_adc = pexConfig.ListField('Prerequisite list for the ADC', str)
    prereq_ins_optics = pexConfig.ListField('Prerequisite list for instrument optics.', str)
    prereq_guider_pos = pexConfig.ListField('Prerequisite list for the guider positioning.', str)
    prereq_guider_adq = pexConfig.ListField('Prerequisite list for the guider adq?', str)
    prereq_tel_settle = pexConfig.ListField('Prerequisite list for telescope settle time.', str)
    prereq_dom_settle = pexConfig.ListField('Prerequisite list for the dome settle time.', str)
    prereq_exposure = pexConfig.ListField('Prerequisite list for exposure time.', str)
    prereq_readout = pexConfig.ListField('Prerequisite list for camera electronics readout time.', str)

    def setDefaults(self):
        """Set defaults for the LSST observatory.
        """
        self.tel_alt_min = 20.0
        self.tel_alt_max = 86.5
        self.tel_az_minpos = -270.0
        self.tel_az_maxpos = 270.0
        self.tel_alt_maxspeed = 3.5
        self.tel_alt_accel = 3.5
        self.tel_alt_decel = 3.5
        self.tel_az_maxspeed = 7.0
        self.tel_az_accel = 7.0
        self.tel_az_decel = 7.0
        self.dom_alt_maxspeed = 1.75
        self.dom_alt_accel = 0.875
        self.dom_alt_decel = 0.875
        self.dom_az_maxspeed = 1.5
        self.dom_az_accel = 0.75
        self.dom_az_decel = 0.75
        self.rotator_minpos = -90.0
        self.rotator_maxpos = 90.0
        self.rotator_followsky = False
        self.rotator_resume_angle_after_filter_change = False
        self.rotator_maxspeed = 3.5
        self.rotator_accel = 1.0
        self.rotator_decel = 1.0
        self.filter_mounttime = 8 * 3600.0
        self.filter_movetime = 120.0
        self.tel_settle_time = 3.0
        self.dome_settle_time = 1.0
        self.camera_readout_time = 2.0
        self.camera_shutter_time = 1.0
        self.tel_optics_ol_slope = 1.0 / 3.5
        self.tel_optics_alt_limit = [0.0, 9.0, 90.0]
        self.tel_optics_cl_delay = [0.0, 20.0]
        self.filter_mounted = ['g', 'r', 'i', 'z', 'y']
        self.filter_pos = 'r'
        self.filter_removable = ['y', 'z']
        self.filter_unmounted = ['u']
        self.prereq_dom_alt = []
        self.prereq_dom_az = []
        self.prereq_tel_alt = []
        self.prereq_tel_az = []
        self.prereq_tel_optics_ol = ['TelAlt', 'TelAz']
        self.prereq_tel_optics_cl = ['DomAlt', 'DomAz', 'Settle', 'Readout', 'TelOpticsOL', 'Filter',
                                     'Rotator']
        self.prereq_rotator = []
        self.prereq_filter = []
        self.prereq_adc = []
        self.prereq_ins_optics = []
        self.prereq_guider_pos = []
        self.prereq_guider_adq = []
        self.prereq_tel_settle = ['TelAlt', 'TelAz']
        self.prereq_dom_settle = []
        self.prereq_exposure = ['TelOpticsCL']
        self.prereq_readout = []
