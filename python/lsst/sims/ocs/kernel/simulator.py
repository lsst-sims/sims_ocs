from builtins import object
from builtins import range
import logging
import math
import time
import collections

from lsst.ts.astrosky.model import Sun

from lsst.ts.astrosky.model import version as astrosky_version
from lsst.ts.dateloc import version as dateloc_version
from lsst.ts.observatory.model import version as obs_mod_version

from lsst.sims.survey.fields import FieldsDatabase, FieldSelection

from lsst.sims.ocs.configuration import ConfigurationCommunicator
from lsst.sims.ocs.database.tables import write_config, write_field
from lsst.sims.ocs.database.tables import write_proposal, write_proposal_field
from lsst.sims.ocs.environment import CloudInterface, SeeingInterface
from lsst.sims.ocs.kernel import DowntimeHandler, ObsProposalHistory
from lsst.sims.ocs.kernel import ProposalInfo, ProposalFieldInfo
from lsst.sims.ocs.kernel import Sequencer, TargetProposalHistory, TimeHandler
from lsst.sims.ocs.sal import SalManager, topic_strdict
from lsst.sims.ocs.setup import LoggingLevel
from lsst.sims.ocs.utilities.constants import DAYS_IN_YEAR, SECONDS_IN_MINUTE
from lsst.sims.ocs.utilities.socs_exceptions import SchedulerTimeoutError
from lsst.ts.scheduler import SALUtils
from lsst.sims.utils import m5_flat_sed

__all__ = ["Simulator"]

FilterSwap = collections.namedtuple('FilterSwap', 'need_swap filter_to_unmount filter_to_mount')

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
    field_database : lsst.sims.survey.fields.FieldsDatabase
        The instance of the fields database.
    field_selection : lsst.sims.survey.fields.FieldSelection
        The instance of the field selector.
    """

    def __init__(self, options, configuration, database, driver=None):
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
            self.conf.survey.duration = self.opts.frac_duration
        self.time_handler = TimeHandler(self.conf.survey.start_date)
        self.log = logging.getLogger("kernel.Simulator")
        if driver is None:
            self.sal = SalManager()
            self.seq = Sequencer(self.conf.observing_site, self.conf.survey.idle_delay)
            self.no_dds_comm = False
        else:
            self.driver =driver
            self.no_dds_comm = True
            self.sal = None
            self.seq = Sequencer(self.conf.observing_site, self.conf.survey.idle_delay, no_dds=self.no_dds_comm)

        self.dh = DowntimeHandler()
        self.conf_comm = ConfigurationCommunicator(no_dds_comm=self.no_dds_comm)
        self.sun = Sun()
        self.cloud_interface = CloudInterface(self.time_handler)
        self.seeing_interface = SeeingInterface(self.time_handler)
        self.field_database = FieldsDatabase()
        self.field_selection = FieldSelection()
        self.obs_site_info = (self.conf.observing_site.longitude, self.conf.observing_site.latitude)
        self.wait_for_scheduler = not self.opts.no_scheduler
        self.observation_proposals_counted = 1
        self.target_proposals_counted = 1
        self.socs_timeout = 180.0  # seconds
        if self.opts.scheduler_timeout > self.socs_timeout:
            self.socs_timeout = self.opts.scheduler_timeout

    @property
    def duration(self):
        """int: The duration of the simulation in days.
        """
        return math.floor(self.fractional_duration * DAYS_IN_YEAR)

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
        if not self.no_dds_comm:
            self.sal.finalize()
        self.log.info("Ending simulation")

    def gather_proposal_history(self, phtype, topic):
        """Gather the proposal history from the current target.

        Parameters
        ----------
        phtype : str
            The type of the proposal history (target or observation).
        topic : :class:`scheduler_targetC` or :class:`scheduler_interestedProposalC`
            The topic instance to gather the observation proposal information from.
        """
        if phtype == "observation":
            for i in range(topic.num_proposals):
                self.db.append_data("observation_proposal_history",
                                    ObsProposalHistory(self.observation_proposals_counted,
                                                       int(topic.proposal_Ids[i]),
                                                       topic.proposal_values[i],
                                                       topic.proposal_needs[i],
                                                       topic.proposal_bonuses[i],
                                                       topic.proposal_boosts[i],
                                                       topic.observationId))
                self.observation_proposals_counted += 1
        if phtype == "target":
            for i in range(topic.num_proposals):
                self.db.append_data("target_proposal_history",
                                    TargetProposalHistory(self.target_proposals_counted,
                                                          int(topic.proposal_Ids[i]),
                                                          topic.proposal_values[i],
                                                          topic.proposal_needs[i],
                                                          topic.proposal_bonuses[i],
                                                          topic.proposal_boosts[i],
                                                          topic.targetId))
                self.target_proposals_counted += 1

    def get_target_from_scheduler(self):
        """Get target from scheduler.

        This function provides the mechanism for getting the target from the
        Scheduler. Currently, a while loop is required to do this.
        """
        if self.no_dds_comm:
            target = self.driver.select_next_target().get_copy()
            SALUtils.wtopic_target(self.target, target, self.driver.science_proposal_list[0].sky)
        else:
            lasttime = time.time()
            while self.wait_for_scheduler:
                rcode = self.sal.manager.getNextSample_target(self.target)
                if rcode == 0 and self.target.num_exposures != 0:
                    break
                else:
                    tf = time.time()
                    if (tf - lasttime) > self.socs_timeout:
                        raise SchedulerTimeoutError("The Scheduler is not serving targets!")

    def initialize(self):
        """Perform initialization steps.

        This function handles initialization of the :class:`.SalManager` and :class:`.Sequencer` instances and
        gathering the necessary telemetry topics.
        """
        self.log.info("Initializing simulation")
        self.log.info("Simulation Session Id = {}".format(self.db.session_id))
        if not self.no_dds_comm:
            self.sal.initialize()
        self.seq.initialize(self.sal, self.conf.observatory)
        self.dh.initialize(self.conf.downtime)
        self.dh.write_downtime_to_db(self.db)
        self.cloud_interface.initialize(self.conf.environment.cloud_db)
        self.seeing_interface.initialize(self.conf.environment, self.conf.observatory.filters)
        self.conf_comm.initialize(self.sal, self.conf)
        if not self.no_dds_comm:
            self.comm_time = self.sal.set_publish_topic("timeHandler")
            self.target = self.sal.set_subscribe_topic("target")
            self.cloud = self.sal.set_publish_topic("cloud")
            self.seeing = self.sal.set_publish_topic("seeing")
            self.filter_swap = self.sal.set_subscribe_topic("filterSwap")
            self.interested_proposal = self.sal.set_subscribe_topic("interestedProposal")
        else:
            from SALPY_scheduler import scheduler_timeHandlerC
            from SALPY_scheduler import scheduler_targetC
            from SALPY_scheduler import scheduler_cloudC
            from SALPY_scheduler import scheduler_seeingC
            from SALPY_scheduler import scheduler_filterSwapC
            from SALPY_scheduler import scheduler_interestedProposalC

            self.comm_time = scheduler_timeHandlerC()
            self.target = scheduler_targetC()
            self.cloud = scheduler_cloudC()
            self.seeing = scheduler_seeingC()
            self.filter_swap = scheduler_filterSwapC()
            self.interested_proposal = scheduler_interestedProposalC()

        self.log.info("Finishing simulation initialization")

    def run(self):
        """Run the simulation.
        """
        self.log.info("Starting simulation")

        if self.no_dds_comm:
            self.configure_driver()
        else:
            self.conf_comm.run()

        self.save_configuration()
        self.save_proposal_information()
        self.save_field_information()

        self.log.debug("Duration = {}".format(self.duration))
        for night in range(1, int(self.duration) + 1):
            self.start_night(night)
            if self.no_dds_comm:
                self.driver.update_time(self.time_handler.current_timestamp, night)
                self.driver.start_night(self.time_handler.current_timestamp, night)

            while self.time_handler.current_timestamp < self.end_of_night:

                if not self.no_dds_comm:
                    self.comm_time.timestamp = self.time_handler.current_timestamp
                    self.sal.put(self.comm_time)

                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Timestamp sent: {:.6f}".format(self.time_handler.current_timestamp))

                observatory_state = self.seq.get_observatory_state(self.time_handler.current_timestamp)
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Observatory State: {}".format(topic_strdict(observatory_state)))
                if self.no_dds_comm:
                    self.driver.update_time(self.time_handler.current_timestamp, night)
                    self.driver.update_internal_conditions(observatory_state, night)
                    self.cloud.cloud = self.cloud_interface.get_cloud(self.time_handler.time_since_start)
                    self.seeing.seeing = self.seeing_interface.get_seeing(self.time_handler.time_since_start)
                    self.driver.update_external_conditions(self.cloud.cloud, self.seeing.seeing)
                else:
                    self.sal.put(observatory_state)

                    self.cloud_interface.set_topic(self.time_handler, self.cloud)
                    self.sal.put(self.cloud)

                    self.seeing_interface.set_topic(self.time_handler, self.seeing)
                    self.sal.put(self.seeing)

                self.get_target_from_scheduler()

                observation, slew_info, exposure_info = self.seq.observe_target(self.target,
                                                                                self.time_handler)
                # Add a few more things to the observation
                observation.night = night
                elapsed_time = self.time_handler.time_since_given(observation.observation_start_time)
                observation.cloud = self.cloud_interface.get_cloud(elapsed_time)
                seeing_values = self.seeing_interface.calculate_seeing(elapsed_time, observation.filter,
                                                                   observation.airmass)
                observation.seeing_fwhm_500 = seeing_values[0]
                observation.seeing_fwhm_geom = seeing_values[1]
                observation.seeing_fwhm_eff = seeing_values[2]

                visit_exposure_time = sum([observation.exposure_times[i]
                                           for i in range(observation.num_exposures)])
                observation.five_sigma_depth = m5_flat_sed(observation.filter,
                                                           observation.sky_brightness,
                                                           observation.seeing_fwhm_eff,
                                                           visit_exposure_time,
                                                           observation.airmass)

                # Pass observation back to scheduler
                self.log.log(LoggingLevel.EXTENSIVE.value, "tx: observation")
                if self.no_dds_comm:
                    driver_observation = SALUtils.rtopic_observation(observation)
                    target_list = self.driver.register_observation(driver_observation)
                    SALUtils.wtopic_interestedProposal(self.interested_proposal,
                                                       observation.targetId,
                                                       target_list)
                else:
                    self.sal.put(observation)

                    # Wait for interested proposal information
                    lastconfigtime = time.time()
                    while self.wait_for_scheduler:
                        rcode = self.sal.manager.getNextSample_interestedProposal(self.interested_proposal)
                        if rcode == 0 and self.interested_proposal.num_proposals >= 0:
                            self.log.log(LoggingLevel.EXTENSIVE.value, "Received interested proposal.")
                            break
                        else:
                            tf = time.time()
                            if (tf - lastconfigtime) > 5.0:
                                self.log.log(LoggingLevel.EXTENSIVE.value,
                                             "Failed to receive interested proposal due to timeout.")
                                break

                if self.wait_for_scheduler and observation.targetId != -1:
                    self.db.append_data("target_history", self.target)
                    self.db.append_data("observation_history", observation)
                    self.gather_proposal_history("target", self.target)
                    self.gather_proposal_history("observation", self.interested_proposal)
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

    def save_configuration(self):
        """Save the configuration information to the DB.
        """
        c = self.conf.config_list()
        c.extend(self.seq.sky_brightness_config())
        if not self.no_dds_comm:
            c.append(("scheduler/version", self.opts.scheduler_version))
        c.append(("dateloc/version", dateloc_version.__version__))
        c.append(("astrosky_model/version", astrosky_version.__version__))
        c.append(("observatory_model/version", obs_mod_version.__version__))
        config_list = [write_config((i + 1, x[0], x[1]), self.db.session_id) for i, x in enumerate(c)]
        self.db.write_table("config", config_list)

    def save_field_information(self):
        """Save the field information to the DB.
        """
        query = self.field_selection.get_all_fields()
        fields = self.field_database.get_field_set(query)
        field_list = [write_field(field, self.db.session_id) for field in sorted(fields)]
        self.db.write_table("field", field_list)

    def save_proposal_information(self):
        """Save the active proposal information to the DB.
        """
        proposals = []
        num_proposals = 1
        proposal_fields = {}
        if self.conf.science.general_props.active is not None:
            for general_config in self.conf.science.general_props.active:
                proposals.append(write_proposal(ProposalInfo(num_proposals, general_config.name, "General"),
                                                self.db.session_id))
                proposal_fields[num_proposals] = general_config.proposal_fields(self.field_database,
                                                                                self.field_selection)
                num_proposals += 1
        if self.conf.science.sequence_props.active is not None:
            for sequence_config in self.conf.science.sequence_props.active:
                proposals.append(write_proposal(ProposalInfo(num_proposals, sequence_config.name, "Sequence"),
                                                self.db.session_id))
                proposal_fields[num_proposals] = sequence_config.proposal_fields()
                num_proposals += 1
        self.db.write_table("proposal", proposals)
        self.write_proposal_fields(proposal_fields)

    def start_day(self):
        """Perform actions at the start of day.

        This function performs all actions at the start of day. This involves:

        * Sending a timestamp to the Scheduler
        * Checking if the Scheduler requests a filter swap
        * Peforming the filter swap if requested
        """
        if not self.no_dds_comm:
            self.comm_time.timestamp = self.time_handler.current_timestamp
            self.sal.put(self.comm_time)
        self.log.debug("Start of day {} at {}".format(self.comm_time.night,
                                                      self.time_handler.current_timestring))
        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Daytime Timestamp sent: {:.6f}".format(self.time_handler.current_timestamp))

        if self.no_dds_comm:
            self.filter_swap = FilterSwap(*self.driver.get_need_filter_swap())
            self.seq.start_day(self.filter_swap)
        else:
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

        self.seq.start_day(self.filter_swap)

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
            self.log.info("Observatory is down: {} days.".format(down_days))
            if not self.no_dds_comm:
                self.comm_time.is_down = True
                self.comm_time.down_duration = down_days
                self.comm_time.timestamp = self.time_handler.current_timestamp
            self.log.log(LoggingLevel.EXTENSIVE.value,
                         "Downtime Start Night Timestamp sent: {:.6f}"
                         .format(self.time_handler.current_timestamp))
            self.sal.put(self.comm_time)
            observatory_state = self.seq.get_observatory_state(self.time_handler.current_timestamp)
            self.log.log(LoggingLevel.EXTENSIVE.value,
                         "Downtime Observatory State: {}".format(topic_strdict(observatory_state)))
            if not self.no_dds_comm:
                self.sal.put(observatory_state)

            delta = math.fabs(self.time_handler.current_timestamp - self.end_of_night) + SECONDS_IN_MINUTE
            self.time_handler.update_time(delta, "seconds")
        elif not self.no_dds_comm:
            self.comm_time.is_down = False
            self.comm_time.down_duration = down_days

    def write_proposal_fields(self, prop_fields):
        """Transform the proposal field information and write to the survey database.

        Parameters
        ----------
        prop_fields : dict
            The set of proposal fields information.
        """
        num_proposal_fields = 1
        data = []
        for prop_id, field_ids in prop_fields.items():
            for field_id in field_ids:
                data.append(write_proposal_field(ProposalFieldInfo(num_proposal_fields,
                                                                   prop_id, field_id),
                                                 self.db.session_id))
                num_proposal_fields += 1
        self.db.write_table("proposal_field", data)

    def configure_driver(self):
        """When running with no DDS communication layer, this function can be used to configure the driver.

        """
        self.driver.configure_duration(self.conf.survey.full_duration)
        self.log.info("run: rx scheduler config survey_duration=%.1f" % (self.conf.survey.full_duration))

        config_dict = SALUtils.rtopic_driver_config(self.conf.sched_driver)
        self.driver.configure(config_dict)
        self.log.info("run: rx driver config=%s" % config_dict)

        config_dict = SALUtils.rtopic_location_config(self.conf_comm.obs_site_conf)
        self.driver.configure_location(config_dict)
        self.log.info("run: rx site config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_telescope_config(self.conf_comm.tel_conf)
        self.driver.configure_telescope(config_dict)
        self.log.info("run: rx telescope config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_dome_config(self.conf_comm.dome_conf)
        self.driver.configure_dome(config_dict)
        self.log.info("run: rx dome config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_rotator_config(self.conf_comm.rot_conf)
        self.driver.configure_rotator(config_dict)
        self.log.info("run: rx rotator config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_camera_config(self.conf_comm.cam_conf)
        self.driver.configure_camera(config_dict)
        self.log.info("run: rx camera config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_slew_config(self.conf_comm.slew_conf)
        self.driver.configure_slew(config_dict)
        self.log.info("run: rx slew config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_optics_config(self.conf_comm.olc_conf)
        self.driver.configure_optics(config_dict)
        self.log.info("run: rx optics config=%s" % (config_dict))

        config_dict = SALUtils.rtopic_park_config(self.conf_comm.park_conf)
        self.driver.configure_park(config_dict)
        self.log.info("run: rx park config=%s" % (config_dict))

        # Configure general proposals
        num_proposals = 1
        from SALPY_scheduler import scheduler_generalPropConfigC
        general_topic = scheduler_generalPropConfigC()
        for prop_name in self.conf.science.general_props.keys():
            self.conf.science.general_props[prop_name].set_topic(general_topic)
            config_dict = SALUtils.rtopic_area_prop_config(general_topic)
            self.log.info("run: rx area prop id=%i name=%s config=%s" % (num_proposals, prop_name,
                                                                        config_dict))
            self.driver.create_area_proposal(num_proposals,
                                            prop_name,
                                            config_dict)
            num_proposals += 1

        from SALPY_scheduler import scheduler_sequencePropConfigC
        sequence_topic = scheduler_sequencePropConfigC()
        for prop_name in self.conf.science.sequence_props.keys():
            self.conf.science.sequence_props[prop_name].set_topic(sequence_topic)
            config_dict = SALUtils.rtopic_seq_prop_config(sequence_topic)
            self.log.info("run: rx seq prop id=%i name=%s config=%s" % (num_proposals, prop_name,
                                                                        config_dict))
            self.driver.create_sequence_proposal(num_proposals,
                                                prop_name,
                                                config_dict)
            num_proposals += 1
