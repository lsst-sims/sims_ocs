import copy
import logging
import math

import palpy

from ts_scheduler.observatoryModel import ObservatoryLocation, ObservatoryModel
from ts_scheduler.schedulerTarget import Target

from lsst.sims.ocs.configuration import Camera, Observatory, ObservingSite
from lsst.sims.ocs.setup import LoggingLevel
from lsst.sims.ocs.observatory import ExposureInformation, SlewHistory

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
        self.exposures_made = 0
        self.exposure_list = None

    def __getattr__(self, name):
        """Find attributes in ts_scheduler.observatorModel.ObservatorModel as well as MainObservatory.
        """
        try:
            return getattr(self.model, name)
        except AttributeError:
            cclass_name = self.__class__.__name__
            aclass_name = self.model.__class__.__name__
            raise AttributeError("'{}' and '{}' objects have no attribute '{}'".format(cclass_name,
                                                                                       aclass_name,
                                                                                       name))

    def calculate_visit_time(self, target):
        """Calculate the visit time from the target and camera information.

        This function calculates the visit time from the current camera configuration parameters
        and the list of effective exposure times from the target. The visit time is calculated as:

        shutter_time = 2.0 * (0.5 * camera shutter time)
        visit_time = sum over number of exposures (shutter_time + effective exposure time)
        visit_time += (number of exposures - 1) * camera readout time

        Parameters
        ----------
        target : SALPY_scheduler.targetTestC
            The Scheduler topic instance holding the target information.

        Returns
        -------
        (float, str)
            The calculated visit time and a unit string (default it seconds).
        """
        self.exposure_list = []
        camera_config = Camera()
        shutter_time = 2.0 * (0.5 * camera_config.shutter_time)

        visit_time = 0.0
        for i in xrange(target.num_exposures):
            effective_exposure_time = target.exposure_times[i]
            visit_time += (shutter_time + effective_exposure_time)
            self.exposures_made += 1
            self.exposure_list.append(ExposureInformation(self.exposures_made, i, effective_exposure_time,
                                                          self.observations_made))

        visit_time += (target.num_exposures - 1) * camera_config.readout_time

        return (visit_time, "seconds")

    def configure(self):
        """Configure the ObservatoryModel parameters.
        """
        self.param_dict.update(Observatory().toDict())
        self.model.configure(self.param_dict)

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
        list[:class:.ExposureInformation`]
            A list of the exposure information from the visit.
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

        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Exposure Times for Target {}: {}".format(target.targetId, list(target.exposure_times)))
        visit_time = self.calculate_visit_time(target)
        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Visit Time for Target {}: {}".format(target.targetId, visit_time[0]))

        time_handler.update_time(*visit_time)

        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Observation {} completed at {}.".format(self.observations_made,
                                                              time_handler.current_timestring))

        return slew_history, self.exposure_list

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

        slew_history = SlewHistory(self.slew_count, initial_slew_state.time, final_slew_state.time,
                                   slew_time[0], math.degrees(slew_distance), self.observations_made)

        return slew_time, slew_history
