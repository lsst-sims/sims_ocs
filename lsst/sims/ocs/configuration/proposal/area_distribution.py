import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BandFilter, SkyRegion

__all__ = ["AreaDistribution"]

class AreaDistribution(pexConfig.Config):
    """Configuration for an area distribution proposal.
    """

    name = pexConfig.Field('Name for the proposal.', str)
    sky_region = pexConfig.ConfigField('Sky selection region for the proposal.', SkyRegion)
    filters = pexConfig.ConfigDictField('Filter configuration for the proposal.', str, BandFilter)
