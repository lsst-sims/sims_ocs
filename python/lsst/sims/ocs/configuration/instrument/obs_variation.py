import lsst.pex.config as pexConfig

__all__ = ["ObservatoryVariation"]

class ObservatoryVariation(pexConfig.Config):
    """Configuration of the observatory variational model.
    """

    apply_variation = pexConfig.Field('Apply the observatory variational model.', bool)
    telescope_change = pexConfig.Field('Change (units=percent) in the telescope kinematic parameters over '
                                       'the life of the survey.', float)
    dome_change = pexConfig.Field('Change (units=percent) in the dome kinematic parameters over the life of '
                                  'the survey.', float)

    def setDefaults(self):
        """Defaults for the observatory variational model configuration.
        """
        self.apply_variation = False
        self.telescope_change = 0.0
        self.dome_change = 0.0
