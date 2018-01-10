from builtins import object
from builtins import range
import logging
import math
import numpy
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
from lsst.sims.ocs.environment import CloudModel, SeeingModel
from lsst.sims.ocs.kernel import DowntimeHandler, ObsProposalHistory
from lsst.sims.ocs.kernel import ProposalInfo, ProposalFieldInfo
from lsst.sims.ocs.kernel import SequencerNoDDS, TargetProposalHistory, TimeHandler
from lsst.sims.ocs.setup import LoggingLevel
from lsst.sims.ocs.utilities.constants import DAYS_IN_YEAR, SECONDS_IN_MINUTE
from lsst.sims.ocs.utilities.socs_exceptions import SchedulerTimeoutError
from lsst.sims.utils import m5_flat_sed
from SALPY_scheduler import scheduler_targetC, scheduler_observationC, scheduler_interestedProposalC
from lsst.ts.observatory.model import Target

__all__ = ["SimulatorNoDDS"]

FilterSwap = collections.namedtuple('FilterSwap', 'need_swap filter_to_unmount filter_to_mount')

class SimulatorNoDDS(object):
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

    def __init__(self, options, configuration, database, driver):
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
        self.driver = driver
        self.seq = SequencerNoDDS(self.conf.observing_site, self.conf.survey.idle_delay)
        self.dh = DowntimeHandler()
        self.sun = Sun()
        self.cloud_model = CloudModel(self.time_handler)
        self.seeing_model = SeeingModel(self.time_handler)
        self.field_database = FieldsDatabase()
        self.field_selection = FieldSelection()
        self.obs_site_info = (self.conf.observing_site.longitude, self.conf.observing_site.latitude)
        self.observation_proposals_counted = 1
        self.target_proposals_counted = 1
        self.night = 0

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
        self.driver.end_night(self.time_handler.current_timestamp,
                              self.night)

    def finalize(self):
        """Perform finalization steps.

        This function handles finalization of the :class:`.SalManager` and :class:`.Sequencer` instances.
        """
        self.seq.finalize()
        self.driver.end_survey()
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
        # FixME
        if phtype == "observation":
            for i in range(topic.num_proposals):
                self.db.append_data("observation_proposal_history",
                                    ObsProposalHistory(self.observation_proposals_counted,
                                                       topic.proposal_Ids[i],
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
                                                          topic.proposal_Ids[i],
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
        target = self.driver.select_next_target().get_copy()
        topicTarget = scheduler_targetC()

        topicTarget.targetId = target.targetid
        topicTarget.groupId = target.groupid
        topicTarget.fieldId = target.fieldid
        topicTarget.filter = target.filter
        topicTarget.request_time = target.time
        topicTarget.ra = target.ra
        topicTarget.dec = target.dec
        topicTarget.angle = target.ang
        topicTarget.num_exposures = target.num_exp
        for i, exptime in enumerate(target.exp_times):
            topicTarget.exposure_times[i] = int(exptime)
        topicTarget.airmass = target.airmass
        topicTarget.sky_brightness = target.sky_brightness
        topicTarget.cloud = target.cloud
        topicTarget.seeing = target.seeing
        topicTarget.slew_time = target.slewtime
        topicTarget.cost = target.cost
        topicTarget.rank = target.rank
        topicTarget.num_proposals = target.num_props
        for i, prop_id in enumerate(target.propid_list):
            topicTarget.proposal_Ids[i] = prop_id
        for i, prop_value in enumerate(target.value_list):
            topicTarget.proposal_values[i] = prop_value
        for i, prop_need in enumerate(target.need_list):
            topicTarget.proposal_needs[i] = prop_need
        for i, prop_bonus in enumerate(target.bonus_list):
            topicTarget.proposal_bonuses[i] = prop_bonus

        prop = self.driver.science_proposal_list[0]
        moon_sun = prop.sky.get_moon_sun_info(numpy.array([target.ra_rad]), numpy.array([target.dec_rad]))
        if moon_sun["moonRA"] is not None:
            topicTarget.moon_ra = math.degrees(moon_sun["moonRA"])
            topicTarget.moon_dec = math.degrees(moon_sun["moonDec"])
            topicTarget.moon_alt = math.degrees(moon_sun["moonAlt"])
            topicTarget.moon_az = math.degrees(moon_sun["moonAz"])
            topicTarget.moon_phase = moon_sun["moonPhase"]
            topicTarget.moon_distance = math.degrees(moon_sun["moonDist"])
            topicTarget.sun_alt = math.degrees(moon_sun["sunAlt"])
            topicTarget.sun_az = math.degrees(moon_sun["sunAz"])
            topicTarget.sun_ra = math.degrees(moon_sun["sunRA"])
            topicTarget.sun_dec = math.degrees(moon_sun["sunDec"])
            topicTarget.solar_elong = math.degrees(moon_sun["solarElong"])

        self.target = topicTarget

    def initialize(self):
        """Perform initialization steps.

        This function handles initialization of the :class:`.SalManager` and :class:`.Sequencer` instances and
        gathering the necessary telemetry topics.
        """
        self.log.info("Initializing simulation")
        self.log.info("Simulation Session Id = {}".format(self.db.session_id))

        self.seq.initialize(scheduler_observationC(), self.conf.observatory)
        self.dh.initialize(self.conf.downtime)
        self.dh.write_downtime_to_db(self.db)
        self.cloud_model.initialize(self.conf.environment.cloud_db)
        self.seeing_model.initialize(self.conf.environment, self.conf.observatory.filters)
        # self.conf_comm.initialize(self.sal, self.conf)
        self.target = scheduler_targetC()  # FIXME: self.sal.set_subscribe_topic("target")
        self.cloud = None  # FIXME: self.sal.set_publish_topic("cloud")
        self.seeing = None  # FIXME: self.sal.set_publish_topic("seeing")
        self.filter_swap = None  # FIXME: self.sal.set_subscribe_topic("filterSwap")
        self.interested_proposal = scheduler_interestedProposalC()  # FIXME: self.sal.set_subscribe_topic("interestedProposal")
        self.log.info("Finishing simulation initialization")

    def run(self):
        """Run the simulation.
        """
        self.log.info("Starting simulation")

        self.save_configuration()
        self.save_proposal_information()
        self.save_field_information()

        # self.driver.start_survey(self.time_handler.current_timestamp, self.night)

        self.log.debug("Duration = {}".format(self.duration))
        for night in range(1, int(self.duration) + 1):
            self.start_night(night)
            self.log.debug('Current time: {}'.format(self.time_handler.current_timestring))
            self.driver.update_time(self.time_handler.current_timestamp, night)
            self.driver.start_night(self.time_handler.current_timestamp, self.night)

            while self.time_handler.current_timestamp < self.end_of_night:

                # self.comm_time.timestamp = self.time_handler.current_timestamp
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Timestamp sent: {:.6f}".format(self.time_handler.current_timestamp))
                # self.sal.put(self.comm_time)

                observatory_state = self.seq.get_observatory_state(self.time_handler.current_timestamp)
                self.log.log(LoggingLevel.EXTENSIVE.value,
                             "Observatory State: {}".format(observatory_state))
                self.driver.update_time(self.time_handler.current_timestamp, night)
                # self.sal.put(observatory_state)
                self.driver.update_internal_conditions(observatory_state, night)

                # self.cloud_model.set_topic(self.time_handler, self.cloud)
                self.cloud = self.cloud_model.get_cloud(self.time_handler.time_since_start)
                # self.sal.put(self.cloud)

                self.seeing = self.seeing_model.get_seeing(self.time_handler.time_since_start)
                # self.sal.put(self.seeing)
                self.driver.update_external_conditions(self.cloud, self.seeing)

                self.get_target_from_scheduler()
                self.log.debug(self.target)

                observation, slew_info, exposure_info = self.seq.observe_target(self.target,
                                                                                self.time_handler)
                # Add a few more things to the observation
                observation.night = night
                elapsed_time = self.time_handler.time_since_given(observation.observation_start_time)
                observation.cloud = self.cloud_model.get_cloud(elapsed_time)
                seeing_values = self.seeing_model.calculate_seeing(elapsed_time, observation.filter,
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
                driver_observation = rtopic_observation(observation)
                target_list = self.driver.register_observation(driver_observation)
                wtopic_interestedProposal(self.interested_proposal,
                                          observation.targetId,
                                          target_list)

                if observation.targetId != -1:
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
        # c.append(("scheduler/version", self.opts.scheduler_version))
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
        # self.comm_time.timestamp = self.time_handler.current_timestamp
        self.log.debug("Start of day {} at {}".format(self.night,
                                                      self.time_handler.current_timestring))
        self.log.log(LoggingLevel.EXTENSIVE.value,
                     "Daytime Timestamp sent: {:.6f}".format(self.time_handler.current_timestamp))
        # self.sal.put(self.comm_time)

        self.filter_swap = FilterSwap(*self.driver.get_need_filter_swap())
        self.seq.start_day(self.filter_swap)

    def start_night(self, night):
        """Perform actions at the start of the night.

        Parameters
        ----------
        night : int
            The current night.
        """
        self.night = night
        self.log.info("Night {}".format(night))
        self.seq.start_night(night, self.duration)
        # self.comm_time.night = night

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
            self.log.log(LoggingLevel.EXTENSIVE.value,
                         "Downtime Start Night Timestamp sent: {:.6f}"
                         .format(self.time_handler.current_timestamp))
            observatory_state = self.seq.get_observatory_state(self.time_handler.current_timestamp)
            self.log.log(LoggingLevel.EXTENSIVE.value,
                         "Downtime Observatory State: {}".format(observatory_state))

            delta = math.fabs(self.time_handler.current_timestamp - self.end_of_night) + SECONDS_IN_MINUTE
            self.time_handler.update_time(delta, "seconds")
        # else:
            # self.comm_time.is_down = False
            # self.comm_time.down_duration = down_days

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


def rtopic_observation(topic_observation):

    observation = Target()
    observation.time = topic_observation.observation_start_time
    observation.targetid = topic_observation.targetId
    observation.fieldid = topic_observation.fieldId
    observation.filter = topic_observation.filter
    observation.num_props = topic_observation.num_proposals
    observation.propid_list = []
    for k in range(observation.num_props):
        observation.propid_list.append(topic_observation.proposal_Ids[k])
    observation.ra_rad = math.radians(topic_observation.ra)
    observation.dec_rad = math.radians(topic_observation.dec)
    observation.ang_rad = math.radians(topic_observation.angle)
    observation.num_exp = topic_observation.num_exposures
    observation.exp_times = []
    for k in range(topic_observation.num_exposures):
        observation.exp_times.append(topic_observation.exposure_times[k])

    return observation


def wtopic_interestedProposal(topic, targetId, target_list):

    topic.observationId = targetId
    topic.num_proposals = len(target_list)
    propid_list = []
    need_list = []
    bonus_list = []
    value_list = []
    propboost_list = []
    for k in range(topic.num_proposals):
        topic.proposal_Ids[k] = target_list[k].propid
        topic.proposal_needs[k] = target_list[k].need
        topic.proposal_bonuses[k] = target_list[k].bonus
        topic.proposal_values[k] = target_list[k].value
        topic.proposal_boosts[k] = target_list[k].propboost
        propid_list.append(target_list[k].propid)
        need_list.append(target_list[k].need)
        bonus_list.append(target_list[k].bonus)
        value_list.append(target_list[k].value)
        propboost_list.append(target_list[k].propboost)
    logstr = ("obsId=%i numprops=%i propid=%s need=%s bonus=%s value=%s propboost=%s" %
              (targetId, topic.num_proposals,
               propid_list, need_list, bonus_list, value_list, propboost_list))
    return logstr
