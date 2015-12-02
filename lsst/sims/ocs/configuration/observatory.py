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
