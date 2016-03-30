import copy
import logging
import math

import palpy

from ts_scheduler.observatoryModel import ObservatoryLocation
from ts_scheduler.observatoryModel.observatoryModel import ObservatoryModel
from ts_scheduler.schedulerTarget import Target

from ..configuration.observatory import Observatory
from ..configuration.obs_site import ObservingSite
from ..setup import LoggingLevel
from .slew_information import SlewHistory

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
        observatory_location = ObservatoryLocation()
        observatory_location.configure({"obs_site": ObservingSite().toDict()})
        self.model = ObservatoryModel(observatory_location)
        self.param_dict = {}
        self.slew_count = 0
        self.observations_made = 0
        # Variables that will disappear as more functionality is added.
        self.visit_time = (34.0, "seconds")

    def configure(self):
        """Configure the ObservatoryModel parameters.
        """
        self.param_dict.update(Observatory().toDict())
        self.model.configure(self.param_dict)

    def slew(self, target):
        """Perform the slewing operation for the observatory to the given target.

        Parameters
        ----------
        target : SALPY_scheduler.targetTestC
            The Scheduler topic instance holding the target information.

        Returns
        -------
        float
            The time to slew the telescope from its current position to the target position.
        :class:`.SlewHistory`
            The slew history information from the current slew.
        """
        self.slew_count += 1
        initial_slew_state = copy.deepcopy(self.model.currentState)
        sched_target = Target.from_topic(target)
        self.model.slew(sched_target)
        final_slew_state = copy.deepcopy(self.model.currentState)

        slew_time = (final_slew_state.time - initial_slew_state.time, "seconds")

        slew_distance = palpy.dsep(final_slew_state.ra_rad, final_slew_state.dec_rad,
                                   initial_slew_state.ra_rad, initial_slew_state.dec_rad)

        slew_history = SlewHistory(self.slew_count, initial_slew_state.time, final_slew_state.time, slew_time,
                                   math.degrees(slew_distance), self.observations_made)

        return slew_time, slew_history

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

        Returns
        -------
        :class:`.SlewHistory`
            The slew history information from the current slew.
        """
        self.observations_made += 1

        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Starting observation {} for target {}.".format(self.observations_made,
                                                                     target.targetId))

        slew_time, slew_history = self.slew(target)
        time_handler.update_time(*slew_time)

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

        return slew_history
