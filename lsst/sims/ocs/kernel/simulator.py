import logging
import math
import time

from ts_scheduler.sky_model import Sun

from lsst.sims.ocs.configuration import ConfigurationCommunicator
from lsst.sims.ocs.database.tables import write_field, write_proposal
from lsst.sims.ocs.environment import CloudModel, SeeingModel
from lsst.sims.ocs.kernel import DowntimeHandler, ProposalHistory, ProposalInfo, Sequencer, TimeHandler
from lsst.sims.ocs.sal import SalManager, topic_strdict
from lsst.sims.ocs.setup import LoggingLevel
from lsst.sims.ocs.utilities.constants import DAYS_IN_YEAR, SECONDS_IN_MINUTE

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
    dh : :class:`.DowntimeHandler`
        The downtime handler instance.
    conf_comm : :class:`.ConfigurationCommunicator`
        The configuration communicator instance.
    cloud_model : :class:`.CloudModel`
        The cloud model instance.
    seeing_model : :class:`.SeeingModel`
        The seeing model instance.
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
            self.fractional_duration = self.conf.survey.duration
        else:
            self.fractional_duration = self.opts.frac_duration
        self.time_handler = TimeHandler(self.conf.survey.start_date)
        self.log = logging.getLogger("kernel.Simulator")
        self.sal = SalManager()
        self.seq = Sequencer(self.conf.observing_site, self.conf.survey.idle_delay)
        self.dh = DowntimeHandler()
        self.conf_comm = ConfigurationCommunicator()
        self.sun = Sun()
        self.cloud_model = CloudModel()
        self.seeing_model = SeeingModel()
        self.obs_site_info = (self.conf.observing_site.longitude, self.conf.observing_site.latitude)
        self.wait_for_scheduler = not self.opts.no_scheduler
        self.proposals_counted = 1

    @property
    def duration(self):
        """int: The duration of the simulation in days.
        """
        return round(self.fractional_duration * DAYS_IN_YEAR)

    def end_night(self):
        """Perform actions at the end of the night.
        """
        self.db.write()
        self.seq.end_night()

    def finalize(self):
        """Perform finalization steps.

        This function handles finalization of the :class:`.SalManager` and :class:`.Sequencer` instances.
        """
        self.seq.finalize()
        self.sal.finalize()
        self.log.info("Ending simulation")

    def gather_proposal_history(self, obsId):
        """Gather the proposal history from the current target.

        Parameters
        ----------
        obsId : int
            The current observation identifier.
        """
        for i in xrange(self.target.num_proposals):
            self.db.append_data("proposal_history", ProposalHistory(self.proposals_counted,
                                                                    self.target.proposal_Ids[i],
                                                                    self.target.proposal_values[i],
                                                                    self.target.proposal_needs[i],
                                                                    self.target.proposal_bonuses[i],
                                                                    self.target.proposal_boosts[i],
                                                                    obsId))
            self.proposals_counted += 1

    def get_target_from_scheduler(self):
        """Get target from scheduler.

        This function provides the mechanism for getting the target from the
        Scheduler. Currently, a while loop is required to do this.
        """
        while self.wait_for_scheduler:
            rcode = self.sal.manager.getNextSample_target(self.target)
            if rcode == 0 and self.target.num_exposures != 0:
                break

    def initialize(self):
        """Perform initialization steps.

        This function handles initialization of the :class:`.SalManager` and :class:`.Sequencer` instances and
        gathering the necessary telemetry topics.
        """
        self.log.info("Initializing simulation")
        self.log.info("Simulation Session Id = {}".format(self.db.session_id))
        self.sal.initialize()
        self.seq.initialize(self.sal, self.conf.observatory)
        self.dh.initialize(self.conf.downtime)
        self.dh.write_downtime_to_db(self.db)
        self.cloud_model.initialize(self.conf.environment.cloud_db)
        # self.cloud_model.write_to_db(self.db)
        self.seeing_model.initialize(self.conf.environment.seeing_db)
        # self.seeing_model.write_to_db(self.db)
        self.conf_comm.initialize(self.sal, self.conf)
        self.comm_time = self.sal.set_publish_topic("timeHandler")
        self.target = self.sal.set_subscribe_topic("target")
        self.field = self.sal.set_subscribe_topic("field")
        self.cloud = self.sal.set_publish_topic("cloud")
        self.seeing = self.sal.set_publish_topic("seeing")
        self.filter_swap = self.sal.set_subscribe_topic("filterSwap")

    def run(self):
        """Run the simulation.
        """
        self.log.info("Starting simulation")

        self.conf_comm.run()
        self.save_proposal_information()

        # Get fields from scheduler
        if self.wait_for_scheduler:
            self.log.info("Retrieving fields from Scheduler")
            field_set = set()
            fields_from_dds = 0
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
                field_set.add((self.field.ID, self.field.fov, self.field.ra, self.field.dec,
                               self.field.gl, self.field.gb, self.field.el, self.field.eb))
                fields_from_dds += 1
                time.sleep(0.00001)

            self.log.info("DDS retrieved {} field messages.".format(fields_from_dds))
            self.field_list = [write_field(field, self.db.session_id) for field in sorted(field_set)]
            self.log.info("{} fields retrieved".format(len(self.field_list)))
            self.log.log(LoggingLevel.EXTENSIVE.value, "{}".format(self.field_list))
            self.db.write_table("field", self.field_list)

        self.log.debug("Duration = {}".format(self.duration))
        for night in xrange(1, int(self.duration) + 1):
            self.start_night(night)

            while self.time_handler.current_timestamp < self.end_of_night:

                self.comm_time.timestamp = self.time_handler.current_timestamp
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Timestamp sent: {}".format(self.time_handler.current_timestring))
                self.sal.put(self.comm_time)

                observatory_state = self.seq.get_observatory_state(self.time_handler.current_timestamp)
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Observatory State: {}".format(topic_strdict(observatory_state)))
                self.sal.put(observatory_state)

                self.cloud_model.set_topic(self.time_handler, self.cloud)
                self.sal.put(self.cloud)

                self.seeing_model.set_topic(self.time_handler, self.seeing)
                self.sal.put(self.seeing)

                self.get_target_from_scheduler()

                observation, slew_info, exposure_info = self.seq.observe_target(self.target,
                                                                                self.time_handler)
                # Add a few more things to the observation
                observation.night = night

                # Pass observation back to scheduler
                self.sal.put(observation)

                if self.wait_for_scheduler and observation.targetId != -1:
                    self.db.append_data("target_history", self.target)
                    self.db.append_data("observation_history", observation)
                    self.gather_proposal_history(observation.observationId)
                    for slew_type, slew_data in slew_info.items():
                        self.log.log(LoggingLevel.TRACE.value, "{}, {}".format(slew_type, type(slew_data)))
                        if isinstance(slew_data, list):
                            for data in slew_data:
                                self.db.append_data(slew_type, data)
                        else:
                            self.db.append_data(slew_type, slew_data)
                    for exposure_type in exposure_info:
                        self.log.log(LoggingLevel.TRACE.value, "Adding {} to DB".format(exposure_type))
                        self.log.log(LoggingLevel.TRACE.value,
                                     "Number of exposures being added: "
                                     "{}".format(len(exposure_info[exposure_type])))
                        for exposure in exposure_info[exposure_type]:
                            self.db.append_data(exposure_type, exposure)

            self.end_night()
            self.start_day()

    def save_proposal_information(self):
        """Save the active proposal information to the DB.
        """
        proposals = []
        num_proposals = 1
        for ad_config in self.conf.science.area_dist_props.active:
            proposals.append(write_proposal(ProposalInfo(num_proposals, ad_config.name, "AreaDistribution"),
                                            self.db.session_id))
            num_proposals += 1
        self.db.write_table("proposal", proposals)

    def start_day(self):
        """Perform actions at the start of day.

        This function performs all actions at the start of day. This involves:

        * Sending a timestamp to the Scheduler
        * Checking if the Scheduler requests a filter swap
        * Peforming the filter swap if requested
        """
        self.comm_time.timestamp = self.time_handler.current_timestamp
        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Daytime Timestamp sent: {}".format(self.time_handler.current_timestring))
        self.sal.put(self.comm_time)

        self.filter_swap = self.sal.get_topic("filterSwap")
        lastconfigtime = time.time()
        while self.wait_for_scheduler:
            rcode = self.sal.manager.getNextSample_filterSwap(self.filter_swap)
            if rcode == 0 and self.filter_swap.filter_to_unmount != '':
                break
            else:
                tf = time.time()
                if (tf - lastconfigtime) > 5.0:
                    break

        if self.wait_for_scheduler and self.filter_swap.need_swap:
            self.seq.start_day(self.filter_swap.filter_to_unmount)

    def start_night(self, night):
        """Perform actions at the start of the night.

        Parameters
        ----------
        night : int
            The current night.
        """
        self.log.info("Night {}".format(night))
        self.seq.start_night(night, self.duration)
        self.comm_time.night = night

        self.seq.sky_model.update(self.time_handler.current_timestamp)
        (set_timestamp,
         rise_timestamp) = self.seq.sky_model.get_night_boundaries(self.conf.sched_driver.night_boundary)

        delta = math.fabs(self.time_handler.current_timestamp - set_timestamp)
        self.time_handler.update_time(delta, "seconds")

        self.log.debug("Start of night {} at {}".format(night, self.time_handler.current_timestring))

        self.end_of_night = rise_timestamp

        end_of_night_str = self.time_handler.future_timestring(0, "seconds", timestamp=self.end_of_night)
        self.log.debug("End of night {} at {}".format(night, end_of_night_str))

        self.db.clear_data()

        down_days = self.dh.get_downtime(night)
        if down_days:
            self.comm_time.is_down = True
            self.comm_time.down_duration = down_days
            self.log.log(LoggingLevel.EXTENSIVE.value,
                         "Timestamp sent: {}".format(self.time_handler.current_timestring))
            self.sal.put(self.comm_time)
            observatory_state = self.seq.get_observatory_state(self.time_handler.current_timestamp)
            self.log.log(LoggingLevel.EXTENSIVE.value,
                         "Observatory State: {}".format(topic_strdict(observatory_state)))
            self.sal.put(observatory_state)

            delta = math.fabs(self.time_handler.current_timestamp - self.end_of_night) + SECONDS_IN_MINUTE
            self.time_handler.update_time(delta, "seconds")
        else:
            self.comm_time.is_down = False
            self.comm_time.down_duration = down_days
