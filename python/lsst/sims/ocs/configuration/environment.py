import lsst.pex.config as pexConfig

__all__ = ["Environment"]

class Environment(pexConfig.Config):
    """Configuration for the seeing and cloud models.
    """

    seeing_db = pexConfig.Field('Alternate database file for the seeing. Must have same format as '
                                'internal database.', str)
    cloud_db = pexConfig.Field('Alternate database file for the seeing. Must have same format as '
                               'internal database.', str)
    telescope_seeing = pexConfig.Field('Design value of the telescope contribution to the seeing '
                                       '(units=arcseconds).', float)
    optical_design_seeing = pexConfig.Field('Design value of the optical path contribution to the seeing '
                                            '(units=arcseconds).', float)
    camera_seeing = pexConfig.Field('Design value of the camera contribution to the seeing '
                                    '(units=arcseconds).', float)
    scale_to_eff = pexConfig.Field('Scale factor to convert seeing to effective.', float)
    geom_eff_factor = pexConfig.Field('Scale factor to convert geometric seeing to effective seeing.',
                                      float)

    def setDefaults(self):
        """Set defaults for the seeing and cloud model configurations.
        """
        self.seeing_db = ""
        self.cloud_db = ""
        self.telescope_seeing = 0.25
        self.optical_design_seeing = 0.08
        self.camera_seeing = 0.3
        self.scale_to_eff = 1.16
        self.geom_eff_factor = 1.04
