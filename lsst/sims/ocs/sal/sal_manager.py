import SALPY_scheduler

class SalManager(object):

    def __init__(self, debug_level=0):
        """Constructor for the SAL Manager class."

        This function is the constructor for the SAL Manager class.

        Args:
            debug_level: An integer for the debugging level of the SALPY sub-system manager.
        """
        self.debug_level = debug_level
        self.manager = None

    def initialize(self):
        """Perform initialization steps.

        This function handles initialization steps for the class.
        """
        self.manager = SALPY_scheduler.SAL_scheduler()
        self.manager.setDebugLevel(self.debug_level)

    def finalize(self):
        """Perform finalization steps.

        This function handles finalization steps for the class.
        """
        self.manager.salShutdown()

    def set_publish_topic(self, topic_short_name):
        """Set the given topic for publishing.

        This function handles the topic publishing setup include retrieval of the associated data structure.

        Args:
            topic_short_name: A string containing the part of the topic name minus the scheduler prefix.

        Returns:
            The data structure associated with the published topic.
        """
        topic_name = "scheduler_{}".format(topic_short_name)
        self.manager.salTelemetryPub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def set_subscribe_topic(self, topic_short_name):
        """Set the given topic for subscribing.

        This function handles the topic subscribing setup include retrieval of the associated data structure.

        Args:
            topic_short_name: A string containing the part of the topic name minus the scheduler prefix.

        Returns:
            The data structure associated with the subscribed topic.
        """
        topic_name = "scheduler_{}".format(topic_short_name)
        self.manager.salTelemetrySub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def put(self, topic_obj):
        """Publish the topic.

        This function does the actual work of publishing the given topic data structure. The type is inferred
        from the topic object itself.

        Args:
            topic_obj: The topic data structure.
        """
        name = str(type(topic_obj)).strip("\"\'<>\'").split("_")[-1][:-1]
        func = getattr(self.manager, "putSample_{}".format(name))
        func(topic_obj)
