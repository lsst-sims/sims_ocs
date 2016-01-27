import logging

from ..observatory.lsst_observatory import LsstObservatory
from ..setup.log import LoggingLevel

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
        self.observations_made = 0
        self.observation = None
        self.observatory_model = LsstObservatory()
        self.log = logging.getLogger("kernel.Sequencer")
        # Variables that will disappear as more functionality is added.
        self.slew_time = (6.0, "seconds")
        self.visit_time = (34.0, "seconds")

    def initialize(self, sal):
        """Perform initialization steps.

        This function handles gathering the observation telemetry topic from the given SalManager instance.

        Parameters
        ----------
        sal : :class:`.SalManager`
            A SalManager instance.
        """
        self.observation = sal.set_publish_topic("observationTest")
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
            An instance of the simluation's TimeHanlder.

        Returns
        -------
        SALPY_scheduler.observationTestC
            An observation telemetry topic containing the observed target parameters.
        """
        self.log.log(LoggingLevel.EXTENSIVE.value, "Received target {}".format(target.targetId))
        self.targets_received += 1

        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Starting observation {} for target {}.".format(self.observations_made,
                                                                     target.targetId))
        th.update_time(*self.slew_time)

        self.observation.observationId = self.observations_made
        self.observation.observationTime = th.current_timestamp
        self.observation.targetId = target.targetId
        self.observation.fieldId = target.fieldId
        self.observation.filter = target.filter
        self.observation.ra = target.ra
        self.observation.dec = target.dec
        self.observation.num_exposures = target.num_exposures

        th.update_time(*self.visit_time)
        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Observation {} completed at {}.".format(self.observations_made,
                                                              th.current_timestring))
        self.observations_made += 1

        return self.observation
