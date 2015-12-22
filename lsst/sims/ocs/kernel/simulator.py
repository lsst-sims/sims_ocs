import logging

from lsst.sims.ocs.configuration.conf_comm import ConfigurationCommunicator
from lsst.sims.ocs.sal.sal_manager import SalManager
from lsst.sims.ocs.kernel.sequencer import Sequencer
from lsst.sims.ocs.kernel.time_handler import DAYS_IN_YEAR
from lsst.sims.ocs.kernel.time_handler import HOURS_IN_DAY
from lsst.sims.ocs.kernel.time_handler import SECONDS_IN_HOUR
from lsst.sims.ocs.kernel.time_handler import TimeHandler
from lsst.sims.ocs.setup.log import LoggingLevel

class Simulator(object):
    """Main class for the survey simulation.

    This class is responsible for setting up, running and shutting down the LSST survey simulation.
    """

    def __init__(self, options, configuration, database):
        """Initialize the class.

        Args:
            options (argparse.Namespace): The instance returned by ArgumentParser containing the command-line
                                          options.
            configuration (SimulationConfig): The :class:`SimulationConfig` instance containing the
                                              simulation configuration.
            database (SocsDatabase): The :class:`SocsDatabase` instance for interacting with the simulation
                                     database.
        """
        self.opts = options
        self.conf = configuration
        self.db = database
        if self.opts.frac_duration == -1:
            self.fractional_duration = self.conf.lsst_survey.duration
        else:
            self.fractional_duration = self.opts.frac_duration
        self.time_handler = TimeHandler(self.conf.lsst_survey.start_date)
        self.log = logging.getLogger("kernel.Simulator")
        self.sal = SalManager()
        self.seq = Sequencer()
        self.conf_comm = ConfigurationCommunicator()
        # Variables that will disappear as more functionality is added.
        self.night_adjust = (19.0, "hours")
        self.hours_in_night = 10.0
        self.wait_for_scheduler = not self.opts.no_scheduler

    @property
    def seconds_in_night(self):
        """The number of seconds in a night.

        Returns:
            float
        """
        return self.hours_in_night * SECONDS_IN_HOUR

    @property
    def hours_in_daylight(self):
        """The number of hours in daylight (day hours - night hours).

        Returns:
            float
        """
        return HOURS_IN_DAY - self.hours_in_night

    @property
    def duration(self):
        """The duration of the simulation in days.

        Returns:
            int
        """
        return round(self.fractional_duration * DAYS_IN_YEAR)

    def initialize(self):
        """Perform initialization steps.

        This function handles initialization of the :class:`SalManager` and :class:`Sequencer` instances and
        gathering the necessary telemetry topics.
        """
        self.log.info("Initializing simulation")
        self.sal.initialize()
        self.seq.initialize(self.sal)
        self.conf_comm.initialize(self.sal, self.conf)
        self.comm_time = self.sal.set_publish_topic("timeHandler")
        self.target = self.sal.set_subscribe_topic("targetTest")
        self.observation = self.sal.set_publish_topic("observationTest")

    def _start_night(self, night):
        self.log.info("Night {}".format(night))

        self.end_of_night = self.time_handler.current_timestamp + self.seconds_in_night
        end_of_night_str = self.time_handler.future_timestring(self.seconds_in_night, "seconds")
        self.log.debug("End of night {} at {}".format(night, end_of_night_str))

        self.db.clear_data()

    def _end_night(self):
        # Run time to next night
        self.time_handler.update_time(self.hours_in_daylight, "hours")
        self.db.write()

    def run(self):
        """Run the simulation.
        """
        self.log.info("Starting simulation")

        self.conf_comm.run()

        self.time_handler.update_time(*self.night_adjust)
        self.comm_time.timestamp = self.time_handler.current_timestamp

        self.log.debug("Duration = {}".format(self.duration))
        for night in xrange(1, int(self.duration) + 1):
            self._start_night(night)

            while self.time_handler.current_timestamp < self.end_of_night:

                self.comm_time.timestamp = self.time_handler.current_timestamp
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Timestamp sent: {}".format(self.time_handler.current_timestring))
                self.sal.put(self.comm_time)

                # Get target from scheduler
                while self.wait_for_scheduler:
                    rcode = self.sal.manager.getNextSample_targetTest(self.target)
                    if rcode == 0 and self.target.num_exposures != 0:
                        break

                observation = self.seq.observe_target(self.target, self.time_handler)
                # Pass observation back to scheduler
                self.sal.put(observation)

                self.db.append_data("target_history", self.target)

            self._end_night()

    def finalize(self):
        """Perform finalization steps.

        This function handles finalization of the :class:`SalManager` and :class:`Sequencer` instances.
        """
        self.seq.finalize()
        self.sal.finalize()
        self.log.info("Ending simulation")
