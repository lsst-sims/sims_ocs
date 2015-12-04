import os

import lsst.pex.config as pexConfig

from .camera import Camera
from .dome import Dome
from .rotator import Rotator
from .slew import Slew
from .telescope import Telescope

__all__ = ["Observatory"]

class Observatory(pexConfig.Config):
    """Configuration of the LSST observatory.
    """

    telescope = pexConfig.ConfigField("The LSST telescope configuration.", Telescope)
    dome = pexConfig.ConfigField("The LSST dome configuration.", Dome)
    rotator = pexConfig.ConfigField("The LSST rotator configuration.", Rotator)
    camera = pexConfig.ConfigField("The LSST camera configuration.", Camera)
    slew = pexConfig.ConfigField("The LSST slew configuration.", Slew)

    def setDefaults(self):
        """Set defaults for the observatory configuration.
        """
        pass

    def save_as(self, save_dir=''):
        """Save the configuration objects to separate files.

        Args:
            save_dir (str): The directory in which to save the configuration files.
        """
        self.telescope.save(os.path.join(save_dir, "telescope.py"))
        self.dome.save(os.path.join(save_dir, "dome.py"))
        self.rotator.save(os.path.join(save_dir, "rotator.py"))
        self.camera.save(os.path.join(save_dir, "camera.py"))
        self.slew.save(os.path.join(save_dir, "slew.py"))
