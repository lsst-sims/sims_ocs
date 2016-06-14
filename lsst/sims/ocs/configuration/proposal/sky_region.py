import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import Selection

__all__ = ["SkyRegion"]

class SkyRegion(pexConfig.Config):
    """Configuration for a proposal's sky region of interest.
    """

    region_selections = pexConfig.ConfigDictField('A list of type selections for sky region determination.',
                                                  int, Selection)
    region_combiners = pexConfig.ListField('A list of logical operations [and, or] that combine the region '
                                           'selections. Must be one less than the number of selections. If '
                                           'only one region, the list is left empty.', str)

    def setDefaults(self):
        """Default specification for a sky region.
        """
        self.region_combiners = []
