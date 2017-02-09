from __future__ import division
import logging

__all__ = ["VariationalModel"]

class VariationalModel(object):
    """Class for handling variation of the Observatory kinematic parameters.

    This class handles varying telescope and dome kinematic parameters over the duration
    of the survey. It uses a linear percentage decrease model for now.
    """

    def __init__(self, config):
        """Initialize the class.

        Parameters
        ----------
        config : class`.Observatory`
            The instance of the observatory configuration.
        """
        self.config = config
        self.log = logging.getLogger("observatory.VariationalModel")

    @property
    def active(self):
        """Determine if variational model is active.

        Returns
        -------
        bool
        """
        return self.config.obs_var.apply_variation

    def modify_parameters(self, night, duration):
        """Modify the observatory parameters according to the model.

        Parameters
        ----------
        night : int
            The current survey observing night.
        duration : int
            The survey duration in days.

        Returns
        -------
        dict
            The modified observatory configuration.
        """
        time_frac = night / duration
        obs_conf = self.config.toDict()

        self.change_speeds_and_accelerations(obs_conf["telescope"], self.config.obs_var.telescope_change,
                                             time_frac)
        self.change_speeds_and_accelerations(obs_conf["dome"], self.config.obs_var.dome_change, time_frac)

        return obs_conf

    def change_speeds_and_accelerations(self, sub_system, change, time_frac):
        """Perform a linear degradation on speeds, accelerations and decelerations.

        Parameters
        ----------
        sub_system : dict
            The sub-system configuration to modify.
        change : float
            The percent change for the calculation.
        time_frac : float
            The fraction of survey completion.
        """
        for key in sub_system.keys():
            if "maxspeed" in key or "accel" in key or "decel" in key:
                sub_system[key] *= (1.0 - (change / 100.) * time_frac)
