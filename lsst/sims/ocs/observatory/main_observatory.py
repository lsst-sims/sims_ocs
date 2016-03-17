import logging

from ts_scheduler.observatoryModel.observatoryModel import ObservatoryModel

from ..configuration.observatory import Observatory
from ..configuration.obs_site import ObservingSite
from ..setup import LoggingLevel

__all__ = ["MainObservatory"]

class MainObservatory(object):
    """Class for the Main Observatory.

    This class is designed to look like the real observatory. In the default case, the observatory
    configuration is the main LSST obesrvatory. It uses the observatory model from the LSST Scheduler
    as its base information. There is an option to add variations onto the parameters and values that
    the model calculates to simulate real world behaviors.

    Attributes
    ----------
    log : logging.Logger
        The logging instance.
    model : ts_scheduler.observatoryModel
        The instance of the Observatory model from the LSST Scheduler.
    param_dict : dict
        The configuration parameters for the Observatory model.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.log = logging.getLogger("observatory.MainObservatory")
        self.model = ObservatoryModel()
        self.param_dict = {}
        self.slew_count = 0
        self.observations_made = 0
        # Variables that will disappear as more functionality is added.
        self.slew_time = (6.0, "seconds")
        self.visit_time = (34.0, "seconds")

    def configure(self):
        """Configure the ObservatoryModel parameters.
        """
        self.param_dict.update(Observatory().toDict())
        self.param_dict["obs_site"] = ObservingSite().toDict()
        self.model.configure(self.param_dict)

    def slew(self, target):
        """Perform the slewing operation for the observatory to the given target.

        Parameters
        ----------
        target : SALPY_scheduler.targetTestC
            The Scheduler topic instance holding the target information.
        """
        self.slew_count += 1
        return self.slew_time[0]

    def observe(self, time_handler, target, observation):
        """Perform the observation of the given target.

        Parameters
        ----------
        time_handler : :class:`.TimeHandler`
            An instance of the simulation's TimeHandler.
        target : SALPY_scheduler.targetTestC
            The Scheduler topic instance holding the target information.
        observation : SALPY_scheduler.observationTestC
            The Scheduler topic instance for recording the observation information.
        """
        self.observations_made += 1

        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Starting observation {} for target {}.".format(self.observations_made,
                                                                     target.targetId))

        time_handler.update_time(*self.slew_time)

        observation.observationId = self.observations_made
        observation.observationTime = time_handler.current_timestamp
        observation.targetId = target.targetId
        observation.fieldId = target.fieldId
        observation.filter = target.filter
        observation.ra = target.ra
        observation.dec = target.dec
        observation.num_exposures = target.num_exposures

        time_handler.update_time(*self.visit_time)

        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Observation {} completed at {}.".format(self.observations_made,
                                                              time_handler.current_timestring))
