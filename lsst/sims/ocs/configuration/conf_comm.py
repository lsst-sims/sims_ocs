import logging

class ConfigurationCommunicator(object):
    """Main class for configuration communication.

    This class handles setting up the configuration DDS topics and publishing them so they can be picked up
    by the Scheduler.

    Attributes:
        sal (sal.SalManager): The object responsible for SAL interaction.
        config (configuration.SimulationConfig): The top-level simulation configuration object.
        log (logging.Logger): The logging object.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.sal = None
        self.config = None
        self.log = logging.getLogger("configuration.ConfigurationCommunicator")

    def initialize(self, sal, config):
        """Perform initialization steps.

        Args:
            sal (sal.SalManager): The instance responsible for SAL interaction.
            config (configuration.SimulationConfig): The top-level simulation configuration instance.
        """
        self.log.info("Initializing configuration communication")
        self.sal = sal
        self.config = config

    def _configure_scheduler(self):
        """Configure and send the Scheduler configuration topic.
        """
        sched_conf = self.sal.set_publish_topic("schedulerConfig")
        # Need root logger to get the log file.
        root_logger = logging.getLogger('')
        log_file = ""
        for handler in root_logger.handlers:
            try:
                log_file = handler.baseFilename
            except AttributeError:
                pass
        self.log.debug("Log file for Scheduler: {}".format(log_file))

        sched_conf.log_file = log_file

        self.sal.put(sched_conf)

    def run(self):
        """Run the configuration communicator.
        """
        self.log.info("Running configuration communication")
        self._configure_scheduler()
