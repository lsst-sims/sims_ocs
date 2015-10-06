import logging

from lsst.sims.ocs.setup.log import configure_logging
import SALPY_scheduler as schedTopics

class Simulator(object):

    def __init__(self, sim_duration):
        """Constructor for the Simulator class.

        This function is the constructor for the Simluator class.

        Args:
            sim_duration: A float value for the simulation duraction in fractions of a year.
        """
        self.fractional_duration = sim_duration
        configure_logging()
        self.log = logging.getLogger("kernel.Simulator")

    @property
    def duration(self):
        """The duration of the simulation in days.

        This property reports the number of days in the simulation.
        """
        return round(self.fractional_duration * 365.0)

    def initialize(self):
        self.manager = schedTopics.SAL_scheduler()
        self.manager.setDebugLevel(0)

    def run(self):
        SLEW_TIME = 6.0
        VISIT_TIME = 34.0
        SECONDS_IN_HOUR = 60.0 * 60.0
        SECONDS_IN_NIGHT = 10.0 * SECONDS_IN_HOUR
        SECONDS_IN_FULL_DAY = 24.0 * SECONDS_IN_HOUR
        WAIT_FOR_SCHEDULER = True

        time_topic = schedTopics.scheduler_timeHandlerC()
        time_topic.timestamp = 1590346800.0  # 2020-05-24 19:00:00
        self.manager.salTelemetryPub("scheduler_timeHandler")

        target_topic = schedTopics.scheduler_targetTestC()
        self.manager.salTelemetrySub("scheduler_targetTest")

        observation_topic = schedTopics.scheduler_observationTestC()
        self.manager.salTelemetryPub("scheduler_observationTest")

        counter = 0
        self.log.debug("Duration = {}".format(self.duration))
        for i in xrange(int(self.duration)):
            self.log.info("Night {}".format(i))
            end_of_night = time_topic.timestamp + SECONDS_IN_NIGHT
            self.log.debug("End of night {} at {}".format(i, end_of_night))
            while time_topic.timestamp <= end_of_night:
                self.manager.putSample_timeHandler(time_topic)

                # Get target from scheduler
                while WAIT_FOR_SCHEDULER:
                    rcode = self.manager.getNextSample_targetTest(target_topic)
                    if rcode == 0 and target_topic.num_exposures != 0:
                        break

                # Observe target
                if 1 > 2:
                    self.log.info("Starting observation {} for target {}.".format(counter,
                                                                                  target_topic.targetId))
                time_topic.timestamp += SLEW_TIME

                observation_topic.observationId = counter
                observation_topic.observationTime = time_topic.timestamp
                observation_topic.targetId = target_topic.targetId
                observation_topic.fieldId = target_topic.fieldId
                observation_topic.filter = target_topic.filter
                observation_topic.ra = target_topic.ra
                observation_topic.dec = target_topic.dec
                observation_topic.num_exposures = target_topic.num_exposures

                time_topic.timestamp += VISIT_TIME
                if 1 > 2:
                    self.log.info("Observation {} completed at {}.".format(counter, time_topic.timestamp))

                # Pass observation back to scheduler
                self.manager.putSample_observationTest(observation_topic)
                counter += 1

            if time_topic.timestamp > end_of_night:
                time_topic.timestamp = end_of_night

            # Run time to next night
            time_topic.timestamp += (SECONDS_IN_FULL_DAY - SECONDS_IN_NIGHT)

    def finalize(self):
        self.manager.salShutdown()
