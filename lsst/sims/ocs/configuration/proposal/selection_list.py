import lsst.pex.config as pexConfig

__all__ = ["SelectionList"]

class SelectionList(pexConfig.Config):
    """Configuration for a time range.
    """

    indexes = pexConfig.ListField('The list of selection indexes.', int)

    def setDefaults(self):
        """Default specification for a time range.
        """
        self.indexes = []
