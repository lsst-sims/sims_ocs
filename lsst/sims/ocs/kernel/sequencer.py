import logging

from lsst.sims.ocs.observatory import MainObservatory
from lsst.sims.ocs.setup import LoggingLevel

__all__ = ["Sequencer"]

class Sequencer(object):
    """Handle the observation of a target.

    This class is responsible for taking a target from the Scheduler and performing the necessary steps to
    make an astronomical observation. It is then responsible for handing that observation back.

    Attributes
    ----------
    targets_received : int
        Counter for the number of targets received by the sequencer.
    observations_made : int
        Counter for the number of observations made by the sequencer.
    observation : SALPY_scheduler.observationC
        DDS topic instance for the observation information.
    log : logging.Logger
        The logging instance.
    """

    def __init__(self, obs_site_config, idle_delay):
        """Initialize the class.

        Parameters
        ----------
        obs_site_config : :class:`.ObservingSite`
            The instance of the observing site configuration.
        idle_delay : float
            The delay time (seconds) to skip forward when no target is received.
        """
        self.targets_received = 0
        self.targets_missed = 0
        self.observation = None
        self.observatory_model = MainObservatory(obs_site_config)
        self.observatory_state = None
        self.log = logging.getLogger("kernel.Sequencer")
        self.idle_delay = (idle_delay, "seconds")

    @property
    def observations_made(self):
        """Get the number of observations made.

        Returns
        -------
        int
        """
        return self.observatory_model.observations_made

    def end_of_night(self):
        """Perform end of night functions.
        """
        # Park the telescope for the day.
        self.observatory_model.reset()

    def get_observatory_state(self, timestamp):
        """Return the observatory state in a DDS topic instance.

        Parameters
        ----------
        timestamp : float
            The current timestamp at the state retrieval request.

        Return
        ------
        SALPY_scheduler.observatoryStateC
        """
        self.observatory_model.update_state(timestamp)
        obs_current_state = self.observatory_model.currentState

        self.observatory_state.timestamp = timestamp
        self.observatory_state.pointing_ra = obs_current_state.ra
        self.observatory_state.pointing_dec = obs_current_state.dec
        self.observatory_state.pointing_angle = obs_current_state.ang
        self.observatory_state.pointing_altitude = obs_current_state.alt
        self.observatory_state.pointing_azimuth = obs_current_state.az
        self.observatory_state.pointing_pa = obs_current_state.pa
        self.observatory_state.pointing_rot = obs_current_state.rot
        self.observatory_state.tracking = obs_current_state.tracking
        self.observatory_state.telescope_altitude = obs_current_state.telalt
        self.observatory_state.telescope_azimuth = obs_current_state.telaz
        self.observatory_state.telescope_rot = obs_current_state.telrot
        self.observatory_state.dome_altitude = obs_current_state.domalt
        self.observatory_state.dome_azimuth = obs_current_state.domaz
        self.observatory_state.filter_position = obs_current_state.filter
        self.observatory_state.filter_mounted = ",".join(obs_current_state.mountedfilters)
        self.observatory_state.filter_unmounted = ','.join(obs_current_state.unmountedfilters)

        return self.observatory_state

    def initialize(self, sal, obs_config):
        """Perform initialization steps.

        This function handles gathering the observation telemetry topic from the given SalManager instance.

        Parameters
        ----------
        sal : :class:`.SalManager`
            A SalManager instance.
        obs_config : :class:`.Observatory`
            The instance of the observatory configuration.
        """
        self.observation = sal.set_publish_topic("observation")
        self.observatory_state = sal.set_publish_topic("observatoryState")
        self.observatory_model.configure(obs_config)

    def finalize(self):
        """Perform finalization steps.

        This function logs the number or targets received and observations made.
        """
        self.log.info("Number of targets received: {}".format(self.targets_received))
        self.log.info("Number of observations made: {}".format(self.observations_made))
        self.log.info("Number of targets missed: {}".format(self.targets_missed))

    def observe_target(self, target, th):
        """Observe the given target.

        This function performs the necessary steps to observe the given target. The current steps are:

          * Update the simulation time after "slewing"
          * Copy target information to observation
          * Update the simulation time after "visit"

        If the targetId is -1, this means a target was not offered by the Scheduler. Time is forwarded
        by the idle delay time and slew and exposure information are set to None. The observation takes the
        target's Id.

        Parameters
        ----------
        target : SALPY_scheduler.targetC
            A target telemetry topic containing the current target information.
        th : :class:`.TimeHandler`
            An instance of the simulation's TimeHandler.

        Returns
        -------
        SALPY_scheduler.observationC
            An observation telemetry topic containing the observed target parameters.
        dict(:class:`.SlewHistory`, :class:`.SlewState`, :class:`.SlewState`, list[:class:`.SlewActivity`])
            A dictionanry of all the slew information from the visit.
        dict(list[:class:`.TargetExposure`], list[:class:`.ObsExposure`])
            A dictionary of all the exposure information from the visit.
        """
        if target.targetId != -1:
            self.log.log(LoggingLevel.EXTENSIVE.value, "Received target {}".format(target.targetId))
            self.targets_received += 1

            slew_info, exposure_info = self.observatory_model.observe(th, target, self.observation)
        else:
            self.log.log(LoggingLevel.EXTENSIVE.value, "No target received!")
            self.observation.observationId = target.targetId
            self.observation.targetId = target.targetId
            slew_info = None
            exposure_info = None
            th.update_time(*self.idle_delay)
            self.targets_missed += 1

        return self.observation, slew_info, exposure_info

    def start_of_day(self, filter_to_unmount):
        """Perform start of day functions.

        Parameters
        ----------
        filter_to_unmount : str
            The filter requested for unmounting.
        """
        self.observatory_model.swap_filter(filter_to_unmount)

    def start_of_night(self, night, duration):
        """Perform start of night functions.

        Parameters
        ----------
        night : int
            The current survey observing night.
        duration : int
            The survey duration in days.
        """
        self.observatory_model.start_of_night(night, duration)
