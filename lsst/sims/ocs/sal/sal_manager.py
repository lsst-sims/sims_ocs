import SALPY_scheduler

class SalManager(object):

    def __init__(self, debug_level=0):
        self.debug_level = debug_level
        self.manager = None

    def initialize(self):
        self.manager = SALPY_scheduler.SAL_scheduler()
        self.manager.setDebugLevel(self.debug_level)

    def finalize(self):
        self.manager.salShutdown()

    def set_publish_topic(self, topic_short_name):
        topic_name = "scheduler_{}".format(topic_short_name)
        self.manager.salTelemetryPub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def set_subscribe_topic(self, topic_short_name):
        topic_name = "scheduler_{}".format(topic_short_name)
        self.manager.salTelemetrySub(topic_name)
        topic = getattr(SALPY_scheduler, "{}C".format(topic_name))
        return topic()

    def put(self, topic_obj):
        name = str(type(topic_obj)).strip("\"\'<>\'").split("_")[-1][:-1]
        func = getattr(self.manager, "putSample_{}".format(name))
        func(topic_obj)
