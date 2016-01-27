import logging

from ts_scheduler.observatoryModel.observatoryModel import ObservatoryModel

from ..configuration.observatory import Observatory
from ..configuration.obs_site import ObservingSite

__all__ = ["LsstObservatory"]

class LsstObservatory(object):
    """Main class for the LSST Observatory.

    This class is designed to look like the real LSST Observatory. It uses the Observatory
    model from the Scheduler as its base information. There is an option to add variations
    onto the parameters and values that the model calculcates to simulate real world behaviors.

    Attributes
    ----------
    log : logging.Logger
        The logging instance.
    model : ts_scheduler.observatoryModel
        The instance of the Observatory model from the LSST Scheduler.
    param_dict : dict
        The configuration parameters for the Observatory model.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.log = logging.getLogger("observatory.LsstObservatory")
        self.model = ObservatoryModel()
        self.param_dict = {}

    def configure(self):
        """Configure the ObservatoryModel parameters.
        """
        self.param_dict.update(Observatory().toDict())
        self.param_dict["obs_site"] = ObservingSite().toDict()
        self.model.configure(self.param_dict)
