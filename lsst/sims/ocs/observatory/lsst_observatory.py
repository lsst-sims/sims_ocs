import logging

from ts_scheduler.observatoryModel import ObservatoryModel

class LsstObservatory(object):
    """Main class for the LSST Observatory.

    This class is designed to look like the real LSST Observatory. It uses the Observatory
    model from the Scheduler as its base information. There is then an option to add variations
    onto the parameters and values that the model calculcates to simulate real world behaviors.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.log = logging.getLogger("observatory.LsstObservatory")
        self.model = ObservatoryModel(self.log)
