import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import Selection, SelectionList, TimeRange

__all__ = ["SkyRegion"]

class SkyRegion(pexConfig.Config):
    """Configuration for a proposal's sky region of interest.
    """

    selections = pexConfig.ConfigDictField('A list of type selections for sky region determination.',
                                           int, Selection)
    combiners = pexConfig.ListField('A list of logical operations [and, or] that combine the region '
                                    'selections. Must be one less than the number of selections. If '
                                    'only one region, the list is left empty.', str)
    time_ranges = pexConfig.ConfigDictField('A collection of time ranges for sky region selection.', int,
                                            TimeRange, optional=True)
    selection_mapping = pexConfig.ConfigDictField('A collection of selection mapping arrays.', int,
                                                  SelectionList, optional=True)

    def setDefaults(self):
        """Default specification for a sky region.
        """
        self.combiners = []
