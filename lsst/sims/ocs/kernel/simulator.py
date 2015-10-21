import logging

from lsst.sims.ocs.sal.sal_manager import SalManager
from lsst.sims.ocs.kernel.time_handler import DAYS_IN_YEAR
from lsst.sims.ocs.kernel.time_handler import TimeHandler
from lsst.sims.ocs.setup.log import LoggingLevel

class Simulator(object):

    def __init__(self, sim_duration):
        """Constructor for the Simulator class.

        This function is the constructor for the Simluator class.

        Args:
            sim_duration: A float value for the simulation duraction in fractions of a year.
        """
        self.fractional_duration = sim_duration
        self.time_handler = TimeHandler("2020-05-24")
        self.log = logging.getLogger("kernel.Simulator")
        self.sal = SalManager()

    @property
    def duration(self):
        """The duration of the simulation in days.

        This property reports the number of days in the simulation.
        """
        return round(self.fractional_duration * DAYS_IN_YEAR)

    def initialize(self):
        self.log.info("Initializing simulation")
        self.sal.initialize()
        self.comm_time = self.sal.set_publish_topic("timeHandler")
        self.target = self.sal.set_subscribe_topic("targetTest")
        self.observation = self.sal.set_publish_topic("observationTest")

    def run(self):
        self.log.info("Starting simulation")
        SLEW_TIME = 6.0
        VISIT_TIME = 34.0

        from lsst.sims.ocs.kernel.time_handler import SECONDS_IN_HOUR

        SECONDS_IN_NIGHT = 10.0 * SECONDS_IN_HOUR
        HOURS_IN_DAYLIGHT = 14.0
        WAIT_FOR_SCHEDULER = True

        self.time_handler.update_time(19.0, "hours")
        self.comm_time.timestamp = self.time_handler.current_timestamp

        self.observations_made = 0
        self.targets_received = 0

        self.log.debug("Duration = {}".format(self.duration))
        for night in xrange(1, int(self.duration) + 1):
            self.log.info("Night {}".format(night))
            end_of_night = self.time_handler.current_timestamp + SECONDS_IN_NIGHT
            end_of_night_str = self.time_handler.future_timestring(SECONDS_IN_NIGHT, "seconds")
            self.log.debug("End of night {} at {}".format(night, end_of_night_str))
            while self.time_handler.current_timestamp < end_of_night:
                self.comm_time.timestamp = self.time_handler.current_timestamp
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Timestamp sent: {}".format(self.time_handler.current_timestring))
                self.sal.put(self.comm_time)

                # Get target from scheduler
                while WAIT_FOR_SCHEDULER:
                    rcode = self.sal.manager.getNextSample_targetTest(self.target)
                    if rcode == 0 and self.target.num_exposures != 0:
                        self.targets_received += 1
                        self.log.debug("Received target {}".format(self.target.targetId))
                        break

                # Observe target
                self.log.debug("Starting observation {} for target {}.".format(self.observations_made,
                                                                               self.target.targetId))
                self.time_handler.update_time(SLEW_TIME, "seconds")

                self.observation.observationId = self.observations_made
                self.observation.observationTime = self.time_handler.current_timestamp
                self.observation.targetId = self.target.targetId
                self.observation.fieldId = self.target.fieldId
                self.observation.filter = self.target.filter
                self.observation.ra = self.target.ra
                self.observation.dec = self.target.dec
                self.observation.num_exposures = self.target.num_exposures

                self.time_handler.update_time(VISIT_TIME, "seconds")
                self.log.debug("Observation {} completed at {}.".format(self.observations_made,
                                                                        self.time_handler.current_timestring))

                # Pass observation back to scheduler
                self.sal.put(self.observation)
                self.observations_made += 1

            # Run time to next night
            self.time_handler.update_time(HOURS_IN_DAYLIGHT, "hours")

    def finalize(self):
        self.log.info("Number of targets received: {}".format(self.targets_received))
        self.log.info("Number of observations made: {}".format(self.observations_made))
        self.sal.finalize()
        self.log.info("Ending simulation")
