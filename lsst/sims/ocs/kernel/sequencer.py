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
    observation : SALPY_scheduler.observationTestC
        DDS topic instance for the observation information.
    log : logging.Logger
        The logging instance.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.targets_received = 0
        self.observation = None
        self.observatory_model = MainObservatory()
        self.observatory_state = None
        self.log = logging.getLogger("kernel.Sequencer")

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

    def get_observatory_state(self):
        """Return the observatory state in a DDS topic instance.

        Return
        ------
        SALPY_scheduler.observatoryStateC
        """
        obs_current_state = self.observatory_model.currentState

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

    def initialize(self, sal):
        """Perform initialization steps.

        This function handles gathering the observation telemetry topic from the given SalManager instance.

        Parameters
        ----------
        sal : :class:`.SalManager`
            A SalManager instance.
        """
        self.observation = sal.set_publish_topic("observationTest")
        self.observatory_state = sal.set_publish_topic("observatoryState")
        self.observatory_model.configure()

    def finalize(self):
        """Perform finalization steps.

        This function logs the number or targets received and observations made.
        """
        self.log.info("Number of targets received: {}".format(self.targets_received))
        self.log.info("Number of observations made: {}".format(self.observations_made))

    def observe_target(self, target, th):
        """Observe the given target.

        This function performs the necessary steps to observe the given target. The current steps are:

          * Update the simulation time after "slewing"
          * Copy target information to observation
          * Update the simulation time after "visit"

        Parameters
        ----------
        target : SALPY_scheduler.targetTestC
            A target telemetry topic containing the current target information.
        th : :class:`.TimeHandler`
            An instance of the simulation's TimeHandler.

        Returns
        -------
        SALPY_scheduler.observationTestC
            An observation telemetry topic containing the observed target parameters.
        :class:`.SlewHistory`
            The slew history information from the current slew.
        """
        self.log.log(LoggingLevel.EXTENSIVE.value, "Received target {}".format(target.targetId))
        self.targets_received += 1

        slew_history = self.observatory_model.observe(th, target, self.observation)

        return self.observation, slew_history
