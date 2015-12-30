import logging

class ConfigurationCommunicator(object):
    """Main class for configuration communication.

    This class handles setting up the configuration DDS topics and publishing them so they can be picked up
    by the Scheduler.

    Attributes
    ----------
    sal : :class:`.SalManager`
        The object responsible for SAL interaction.
    config: :class:`.SimulationConfig`
        The top-level simulation configuration object.
    log : logging.Logger
        The logging instance.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.sal = None
        self.config = None
        self.log = logging.getLogger("configuration.ConfigurationCommunicator")

    def initialize(self, sal, config):
        """Perform initialization steps.

        Parameters
        ----------
        sal : :class:`.SalManager`
            The instance responsible for SAL interaction.
        config : :class:`.SimulationConfig`
            The top-level simulation configuration instance.
        """
        self.log.info("Initializing configuration communication")
        self.sal = sal
        self.config = config

    def _configure_scheduler(self):
        """Configure and send the Scheduler configuration topic.
        """
        sched_conf = self.sal.set_publish_topic("schedulerConfig")
        # Need root logger to get the log file.
        root_logger = logging.getLogger('')
        log_file = ""
        for handler in root_logger.handlers:
            try:
                log_file = handler.baseFilename
            except AttributeError:
                pass
        self.log.debug("Log file for Scheduler: {}".format(log_file))

        sched_conf.log_file = log_file

        self.sal.put(sched_conf)

    def _configure_observing_site(self):
        """Configure and send the Observing Site configuration topic.
        """
        obs_site_conf = self.sal.set_publish_topic("obsSiteConfig")

        obs_site_conf.name = self.config.observing_site.name
        obs_site_conf.latitude = self.config.observing_site.latitude
        obs_site_conf.longitude = self.config.observing_site.longitude
        obs_site_conf.height = self.config.observing_site.height
        obs_site_conf.pressure = self.config.observing_site.pressure
        obs_site_conf.temperature = self.config.observing_site.temperature
        obs_site_conf.relativeHumidity = self.config.observing_site.relativeHumidity

        self.sal.put(obs_site_conf)

    def _configure_telescope(self):
        """Configure and send the Telescope configuration topic.
        """
        tel_conf = self.sal.set_publish_topic("telescopeConfig")

        tel_conf.altitude_minpos = self.config.observatory.telescope.altitude_minpos
        tel_conf.altitude_maxpos = self.config.observatory.telescope.altitude_maxpos
        tel_conf.altitude_maxspeed = self.config.observatory.telescope.altitude_maxspeed
        tel_conf.altitude_accel = self.config.observatory.telescope.altitude_accel
        tel_conf.altitude_decel = self.config.observatory.telescope.altitude_decel
        tel_conf.azimuth_minpos = self.config.observatory.telescope.azimuth_minpos
        tel_conf.azimuth_maxpos = self.config.observatory.telescope.azimuth_maxpos
        tel_conf.azimuth_maxspeed = self.config.observatory.telescope.azimuth_maxspeed
        tel_conf.azimuth_accel = self.config.observatory.telescope.azimuth_accel
        tel_conf.azimuth_decel = self.config.observatory.telescope.azimuth_decel
        tel_conf.settle_time = self.config.observatory.telescope.settle_time

        self.sal.put(tel_conf)

    def _configure_dome(self):
        """Configure and send the dome configuration topic.
        """
        dome_conf = self.sal.set_publish_topic("domeConfig")

        dome_conf.altitude_maxspeed = self.config.observatory.dome.altitude_maxspeed
        dome_conf.altitude_accel = self.config.observatory.dome.altitude_accel
        dome_conf.altitude_decel = self.config.observatory.dome.altitude_decel
        dome_conf.azimuth_maxspeed = self.config.observatory.dome.azimuth_maxspeed
        dome_conf.azimuth_accel = self.config.observatory.dome.azimuth_accel
        dome_conf.azimuth_decel = self.config.observatory.dome.azimuth_decel
        dome_conf.settle_time = self.config.observatory.dome.settle_time

        self.sal.put(dome_conf)

    def _configure_rotator(self):
        """Configure and send the rotator configuration topic.
        """
        rot_conf = self.sal.set_publish_topic("rotatorConfig")

        rot_conf.minpos = self.config.observatory.rotator.minpos
        rot_conf.maxpos = self.config.observatory.rotator.maxpos
        rot_conf.maxspeed = self.config.observatory.rotator.maxspeed
        rot_conf.accel = self.config.observatory.rotator.accel
        rot_conf.decel = self.config.observatory.rotator.decel
        rot_conf.follow_sky = self.config.observatory.rotator.follow_sky
        rot_conf.resume_angle = self.config.observatory.rotator.resume_angle

        self.sal.put(rot_conf)

    def _configure_camera(self):
        """Configure and send the camera configuration topic.
        """
        cam_conf = self.sal.set_publish_topic("cameraConfig")

        cam_conf.readout_time = self.config.observatory.camera.readout_time
        cam_conf.shutter_time = self.config.observatory.camera.shutter_time
        cam_conf.filter_mount_time = self.config.observatory.camera.filter_mount_time
        cam_conf.filter_change_time = self.config.observatory.camera.filter_change_time
        cam_conf.filter_mounted = self.config.observatory.camera.filter_mounted_str
        cam_conf.filter_pos = self.config.observatory.camera.filter_pos
        cam_conf.filter_removable = self.config.observatory.camera.filter_removable_str
        cam_conf.filter_unmounted = self.config.observatory.camera.filter_unmounted_str

        self.sal.put(cam_conf)

    def _configure_slew(self):
        """Configure and send the slew configuration topic.
        """
        slew_conf = self.sal.set_publish_topic("slewConfig")

        slew_conf.tel_optics_ol_slope = self.config.observatory.slew.tel_optics_ol_slope
        self.config.observatory.slew.set_array(slew_conf, "tel_optics_cl_alt_limit")
        self.config.observatory.slew.set_array(slew_conf, "tel_optics_cl_delay")
        slew_conf.prereq_dom_alt = self.config.observatory.slew.get_string_rep("prereq_dom_alt")
        slew_conf.prereq_dom_az = self.config.observatory.slew.get_string_rep("prereq_dom_az")
        slew_conf.prereq_tel_alt = self.config.observatory.slew.get_string_rep("prereq_tel_alt")
        slew_conf.prereq_tel_az = self.config.observatory.slew.get_string_rep("prereq_tel_az")
        slew_conf.prereq_tel_optics_ol = self.config.observatory.slew.get_string_rep("prereq_tel_optics_ol")
        slew_conf.prereq_tel_optics_cl = self.config.observatory.slew.get_string_rep("prereq_tel_optics_cl")
        slew_conf.prereq_tel_rot = self.config.observatory.slew.get_string_rep("prereq_tel_rot")
        slew_conf.prereq_filter = self.config.observatory.slew.get_string_rep("prereq_filter")
        slew_conf.prereq_adc = self.config.observatory.slew.get_string_rep("prereq_adc")
        slew_conf.prereq_ins_optics = self.config.observatory.slew.get_string_rep("prereq_ins_optics")
        slew_conf.prereq_guider_pos = self.config.observatory.slew.get_string_rep("prereq_guider_pos")
        slew_conf.prereq_guider_adq = self.config.observatory.slew.get_string_rep("prereq_guider_adq")
        slew_conf.prereq_tel_settle = self.config.observatory.slew.get_string_rep("prereq_tel_settle")
        slew_conf.prereq_dom_az_settle = self.config.observatory.slew.get_string_rep("prereq_dom_az_settle")
        slew_conf.prereq_exposure = self.config.observatory.slew.get_string_rep("prereq_exposure")
        slew_conf.prereq_readout = self.config.observatory.slew.get_string_rep("prereq_readout")

        self.sal.put(slew_conf)

    def _configure_park(self):
        """Configure and send the park position configuration.
        """
        park_conf = self.sal.set_publish_topic("parkConfig")

        park_conf.telescope_altitude = self.config.observatory.park.telescope_altitude
        park_conf.telescope_azimuth = self.config.observatory.park.telescope_azimuth
        park_conf.telescope_rotator = self.config.observatory.park.telescope_rotator
        park_conf.dome_altitude = self.config.observatory.park.dome_altitude
        park_conf.dome_azimuth = self.config.observatory.park.dome_azimuth
        park_conf.filter_position = self.config.observatory.park.filter_position

        self.sal.put(park_conf)

    def run(self):
        """Run the configuration communicator.
        """
        self.log.info("Running configuration communication")
        self._configure_scheduler()
        self._configure_observing_site()
        self._configure_telescope()
        self._configure_dome()
        self._configure_rotator()
        self._configure_camera()
        self._configure_slew()
        self._configure_park()
