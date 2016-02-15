import logging
import math
import time

from ts_scheduler.sky_model import Sun

from ..configuration.conf_comm import ConfigurationCommunicator
from ..database.tables.write_tbls import write_field
from ..kernel.sequencer import Sequencer
from ..kernel.time_handler import DAYS_IN_YEAR
from ..kernel.time_handler import HOURS_IN_DAY
from ..kernel.time_handler import SECONDS_IN_HOUR
from ..kernel.time_handler import TimeHandler
from ..sal.sal_manager import SalManager
from ..setup.log import LoggingLevel

__all__ = ["Simulator"]

class Simulator(object):
    """Main class for the survey simulation.

    This class is responsible for setting up, running and shutting down the LSST survey simulation.

    Attributes
    ----------
    opts : argparse.Namespace
        The options returned by the ArgumentParser instance.
    conf : :class:`.SimulationConfig`
        The simulation configuration instance.
    db : :class:`.SocsDatabase`
        The simulation database instance.
    fractional_duration : float
        The length in years for the simulated survey.
    time_handler : :class:`.TimeHandler`
        The simulation time handling instance.
    log : logging.Logger
        The logging instance.
    sal : :class:`.SalManager`
        The instance that manages interactions with the SAL.
    seq : :class:`.Sequencer`
        The sequencer instance.
    conf_comm : :class:`.ConfigurationCommunicator`
        The configuration communicator instance.
    """

    def __init__(self, options, configuration, database):
        """Initialize the class.

        Parameters
        ----------
        options : argparse.Namespace
            The instance returned by ArgumentParser containing the command-line options.
        configuration : :class:`.SimulationConfig`
            The simulation configuration instance.
        database : :class:`.SocsDatabase`
            The simulation database instance.
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
        self.sun = Sun()
        self.obs_site_info = (self.conf.observing_site.longitude, self.conf.observing_site.latitude)
        self.wait_for_scheduler = not self.opts.no_scheduler

    @property
    def duration(self):
        """int: The duration of the simulation in days.
        """
        return round(self.fractional_duration * DAYS_IN_YEAR)

    def initialize(self):
        """Perform initialization steps.

        This function handles initialization of the :class:`.SalManager` and :class:`.Sequencer` instances and
        gathering the necessary telemetry topics.
        """
        self.log.info("Initializing simulation")
        self.sal.initialize()
        self.seq.initialize(self.sal)
        self.conf_comm.initialize(self.sal, self.conf)
        self.comm_time = self.sal.set_publish_topic("timeHandler")
        self.target = self.sal.set_subscribe_topic("targetTest")
        self.field = self.sal.set_subscribe_topic("field")

    def _start_night(self, night):
        """Perform actions at the start of the night.

        Parameters
        ----------
        night : int
            The current night.
        """
        self.log.info("Night {}".format(night))
        self.log.debug("Start of night {} at {}".format(night, self.time_handler.current_timestring))

        seconds_in_night = self.get_seconds_in_night()
        self.end_of_night = self.time_handler.current_timestamp + seconds_in_night
        end_of_night_str = self.time_handler.future_timestring(seconds_in_night, "seconds")

        self.log.debug("End of night {} at {}".format(night, end_of_night_str))

        self.db.clear_data()

    def _end_night(self):
        """Perform actions at the end of the night.
        """
        self.db.write()
        # Run time to next night
        self.time_handler.update_time(self.get_seconds_in_day(), "seconds")

    def move_to_first_dusk(self):
        """Move simulation to first dusk."
        """
        (_, set_naut_twi) = self.sun.nautical_twilight(self.time_handler.current_timestamp,
                                                       *self.obs_site_info)
        self.time_handler.update_time(set_naut_twi, "hours")

    def get_seconds_in_night(self):
        """float: The number of seconds in the current night.
        """
        (rise_naut_twi,
         set_naut_twi) = self.sun.nautical_twilight(self.time_handler.current_midnight_timestamp,
                                                    *self.obs_site_info)
        if set_naut_twi > HOURS_IN_DAY:
            set_naut_twi -= HOURS_IN_DAY

        hours_in_night = math.fabs(rise_naut_twi - set_naut_twi)
        return hours_in_night * SECONDS_IN_HOUR

    def get_seconds_in_day(self):
        """float: The number of seconds in the current day.
        """
        (rise_naut_twi, set_naut_twi) = self.sun.nautical_twilight(self.time_handler.next_midnight_timestamp,
                                                                   *self.obs_site_info)
        if set_naut_twi > HOURS_IN_DAY:
            set_naut_twi -= HOURS_IN_DAY

        hours_in_day = HOURS_IN_DAY - math.fabs(rise_naut_twi - set_naut_twi)
        return hours_in_day * SECONDS_IN_HOUR

    def run(self):
        """Run the simulation.
        """
        self.log.info("Starting simulation")

        self.conf_comm.run()

        # Get fields from scheduler
        if self.wait_for_scheduler:
            self.log.info("Retrieving fields from Scheduler")
            self.field_list = []
            end_fields = False
            while True:
                rcode = self.sal.manager.getNextSample_field(self.field)
                if self.field.ID == 0:
                    continue
                self.log.log(LoggingLevel.EXTENSIVE.value, self.field.ID)
                if rcode == 0 and self.field.ID == -1:
                    if end_fields:
                        break
                    else:
                        end_fields = True
                        continue
                self.field_list.append(write_field(self.field))
                time.sleep(0.00075)
            self.log.info("{} fields retrieved".format(len(self.field_list)))
            self.db.write_table("field", self.field_list)

        self.move_to_first_dusk()
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

                if self.wait_for_scheduler:
                    self.db.append_data("target_history", self.target)
                    self.db.append_data("observation_history", observation)

            self._end_night()

    def finalize(self):
        """Perform finalization steps.

        This function handles finalization of the :class:`.SalManager` and :class:`.Sequencer` instances.
        """
        self.seq.finalize()
        self.sal.finalize()
        self.log.info("Ending simulation")
