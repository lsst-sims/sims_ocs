from builtins import object
from builtins import str
import SALPY_scheduler

__all__ = ["SalManager"]

class SalManager(object):
    """Handle SAL interactions.

    This class is responsible for most of the interactions with the SAL for DDS communications.
    """

    def __init__(self, debug_level=0):
        """Initialize the class.

        Parameters
        ----------
        debug_level : int
            The debugging level of the SALPY sub-system manager.
        """
        self.debug_level = debug_level
        self.manager = None

    def initialize(self):
        """Perform initialization steps.

        This function handles creation of the Scheduler SAL manager and sets the debugging level.
        """
        self.manager = SALPY_scheduler.SAL_scheduler()
        self.manager.setDebugLevel(self.debug_level)

    def finalize(self):
        """Perform finalization steps.

        This function shuts down the Scheduler SAL manager.
        """
        self.manager.salShutdown()

    def get_topic(self, topic_short_name):
        """Get the given topic.

        This function retrieves the associated data structure for the topic.

        Parameters
        ----------
        topic_short_name : str
            The part of the topic name minus the scheduler prefix.

        Returns
        -------
        SALPY_scheduler.<topic_short_name>C
            The telemetry data structure associated with the topic.
        """
        topic_name = "scheduler_{}".format(topic_short_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def set_publish_topic(self, topic_short_name):
        """Set the given topic for publishing.

        This function handles the topic publishing setup include retrieval of the associated data structure.

        Parameters
        ----------
        topic_short_name : str
            The part of the topic name minus the scheduler prefix.

        Returns
        -------
        SALPY_scheduler.<topic_short_name>C
            The telemetry data structure associated with the published topic.
        """
        topic_name = "scheduler_{}".format(topic_short_name)
        self.manager.salTelemetryPub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def set_subscribe_topic(self, topic_short_name):
        """Set the given topic for subscribing.

        This function handles the topic subscribing setup include retrieval of the associated data structure.

        Parameters
        ----------
        topic_short_name: str
            The part of the topic name minus the scheduler prefix.

        Returns
        -------
        SALPY_scheduler.<topic_short_name>C
            The telemetry data structure associated with the subscribed topic.
        """
        topic_name = "scheduler_{}".format(topic_short_name)
        self.manager.salTelemetrySub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def set_subscribe_logevent(self, event_short_name):
        """Set the given topic for subscribing.

        This function handles the topic subscribing setup include retrieval of the associated data structure.

        Parameters
        ----------
        topic_short_name: str
            The part of the topic name minus the scheduler prefix.

        Returns
        -------
        SALPY_scheduler.<topic_short_name>C
            The telemetry data structure associated with the subscribed topic.
        """
        topic_name = "scheduler_logevent_{}".format(event_short_name)
        self.manager.salEventSub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def put(self, topic_obj):
        """Publish the topic.

        This function does the actual work of publishing the given telemetry topic data structure. The type
        is inferred from the topic object itself.

        Parameters
        ----------
        topic_obj : SALPY_scheduler.<topic_obj>
            The telemetry topic data structure.
        """
        name = str(type(topic_obj)).strip("\"\'<>\'").split("_")[-1][:-1]
        func = getattr(self.manager, "putSample_{}".format(name))
        func(topic_obj)

    def send_command(self, cmd, **kwargs):

        self.manager.salProcessor("scheduler_command_{}".format(cmd))
        # Get the myData object
        self.cmd_topic = getattr(SALPY_scheduler, 'scheduler_command_{}C'.format(cmd))()

        # cmd_topic = self.update_myData(myData,**kwargs)
        for key in kwargs:
            setattr(self.cmd_topic, key, kwargs[key])

        # Make it visible outside
        self.issueCommand = getattr(self.manager, 'issueCommand_{}'.format(cmd))
        self.waitForCompletion = getattr(self.manager, 'waitForCompletion_{}'.format(cmd))

        self.cmdId = self.issueCommand(self.cmd_topic)
        # cmdId_time = time.time()
        # if wait_command:
        #     LOGGER.info("Will wait for Command Completion")
        # waitForCompletion_Command()
        # else:
        #     LOGGER.info("Will NOT wait Command Completion")
