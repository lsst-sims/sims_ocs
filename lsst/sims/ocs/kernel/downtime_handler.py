import logging

from lsst.sims.ocs.downtime.scheduled_downtime import ScheduledDowntime
from lsst.sims.ocs.downtime.unscheduled_downtime import UnscheduledDowntime
from lsst.sims.ocs.setup import LoggingLevel

class DowntimeHandler(object):
    """Coordinate the handling of all the downtime information.

    This class handles the coordination between the scheduled and unscheduled
    downtime information.

    Attributes
    ----------
    scheduled : :class:`.ScheduledDowntime`
        The scheduled downtime information instance.
    unscheduled : :class:`.UnscheduledDowntime`
        The unscheduled downtime information instance.
    current_scheduled : tuple or None
        The set of current scheduled downtime information.
    current_unscheduled : tuple or None
        The set of current unscheduled downtime information.
    log : Log
        The handle for the logger.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.scheduled = ScheduledDowntime()
        self.unscheduled = UnscheduledDowntime()
        self.current_scheduled = None
        self.current_unscheduled = None
        self.log = logging.getLogger("kernel.DowntimeHandler")

    def initialize(self, survey_duration):
        """Perform initialization steps.

        Parameters
        ----------
        survey_duration : int
            The number of days for the survey duration.
        """
        self.scheduled.initialize()
        self.unscheduled.initialize(survey_duration)

    def get_downtime(self, night):
        """Determine if there is downtime for the given night.

        This function looks at the given

        Parameters
        ----------
        night : int
            The night to check the downtime information for.

        Returns
        -------
        int
            The number of downtime nights.
        """
        if self.current_unscheduled is None:
            self.current_unscheduled = self.unscheduled()
        if self.current_scheduled is None:
            self.current_scheduled = self.scheduled()

        downtime_days = 0
        end_downtime_night = -1

        # No more downtime
        if self.current_scheduled is None and self.current_unscheduled is None:
            return downtime_days

        if self.current_scheduled is not None:
            if night == self.current_scheduled[0]:
                end_downtime_night = night + self.current_scheduled[1] - 1
                downtime_days = self.current_scheduled[1]
                self.current_scheduled = None

                if self.current_unscheduled is not None:
                    start_night = self.current_unscheduled[0]
                    end_night = start_night + self.current_unscheduled[1] - 1
                    if start_night >= night and start_night <= end_downtime_night:
                        if end_night > end_downtime_night:
                            partial = end_night - end_downtime_night
                            downtime_days += partial
                            self.log.log(LoggingLevel.EXTENSIVE.value,
                                         "Partial overlapping unscheduled downtime: {}".format(partial))
                        else:
                            self.log.log(LoggingLevel.EXTENSIVE.value,
                                         "Completely overlapping unscheduled downtime")

                        self.current_unscheduled = None
                return downtime_days

        if self.current_unscheduled is not None:
            if night == self.current_unscheduled[0]:
                end_downtime_night = night + self.current_unscheduled[1] - 1
                downtime_days = self.current_unscheduled[1]
                self.current_unscheduled = None

                if self.current_scheduled is not None:
                    start_night = self.current_scheduled[0]
                    end_night = start_night + self.current_scheduled[1] - 1
                    if start_night >= night and start_night <= end_downtime_night:
                        if end_night > end_downtime_night:
                            partial = end_night - end_downtime_night
                            downtime_days += partial
                            self.log.log(LoggingLevel.EXTENSIVE.value,
                                         "Partial overlapping scheduled downtime: {}".format(partial))
                        else:
                            self.log.log(LoggingLevel.EXTENSIVE.value,
                                         "Completely overlapping scheduled downtime")
                        self.current_scheduled = None
                return downtime_days

        # Downtime available, but none tonight.
        return downtime_days
