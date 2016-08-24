import lsst.pex.config as pexConfig

__all__ = ["Environment"]

class Environment(pexConfig.Config):
    """Configuration for the seeing and cloud models.
    """

    seeing_db = pexConfig.Field('Alternate database file for the seeing. Must have same format as '
                                'internal database.', str)

    def setDefaults(self):
        """Set defaults for the seeing anf cloud model configurations.
        """
        self.seeing_db = ""
