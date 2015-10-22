import logging

class Sequencer(object):

    def __init__(self):
        self.targets_received = 0
        self.observations_made = 0
        self.observation = None
        self.log = logging.getLogger("kernel.Sequencer")
        # Variables that will disappear as more functionality is added.
        self.slew_time = (6.0, "seconds")
        self.visit_time = (40.0, "seconds")

    def initialize(self, sal):
        self.observation = sal.set_publish_topic("observationTest")

    def finalize(self):
        self.log.info("Number of targets received: {}".format(self.targets_received))
        self.log.info("Number of observations made: {}".format(self.observations_made))

    def observe_target(self, target, th):
        self.log.debug("Received target {}".format(target.targetId))
        self.targets_received += 1

        self.log.debug("Starting observation {} for target {}.".format(self.observations_made,
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
        self.log.debug("Observation {} completed at {}.".format(self.observations_made,
                                                                th.current_timestring))
        self.observations_made += 1

        return self.observation
