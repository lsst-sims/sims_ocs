import os

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import load_config
from lsst.sims.ocs.configuration.instrument import Camera, Dome, Park, ObservatoryVariation
from lsst.sims.ocs.configuration.instrument import Rotator, Slew, Telescope

__all__ = ["Observatory"]

class Observatory(pexConfig.Config):
    """Configuration of the LSST observatory.
    """

    telescope = pexConfig.ConfigField("The LSST telescope configuration.", Telescope)
    dome = pexConfig.ConfigField("The LSST dome configuration.", Dome)
    rotator = pexConfig.ConfigField("The LSST rotator configuration.", Rotator)
    camera = pexConfig.ConfigField("The LSST camera configuration.", Camera)
    slew = pexConfig.ConfigField("The LSST slew configuration.", Slew)
    park = pexConfig.ConfigField("The LSST observatory park position configuration.", Park)
    obs_var = pexConfig.ConfigField("The observatory variational model configuration", ObservatoryVariation)

    def setDefaults(self):
        """Set defaults for the observatory configuration.
        """
        pass

    def load(self, config_files):
        """Load the configuration override files.

        Parameters
        ----------
        config_files : list[str]
            A set of configuration override files.
        """
        load_config(self.telescope, config_files)
        load_config(self.dome, config_files)
        load_config(self.rotator, config_files)
        load_config(self.camera, config_files)
        load_config(self.slew, config_files)
        load_config(self.park, config_files)
        load_config(self.obs_var, config_files)

    def save_as(self, save_dir=''):
        """Save the configuration objects to separate files.

        Parameters
        ----------
        save_dir : str
            The directory in which to save the configuration files.
        """
        self.telescope.save(os.path.join(save_dir, "telescope.py"))
        self.dome.save(os.path.join(save_dir, "dome.py"))
        self.rotator.save(os.path.join(save_dir, "rotator.py"))
        self.camera.save(os.path.join(save_dir, "camera.py"))
        self.slew.save(os.path.join(save_dir, "slew.py"))
        self.park.save(os.path.join(save_dir, "park.py"))
        self.obs_var.save(os.path.join(save_dir, "obs_variation.py"))
