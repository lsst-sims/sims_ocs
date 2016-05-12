import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import AreaDistribution

__all__ = ["area_dist_prop_reg"]

area_dist_prop_reg = pexConfig.makeRegistry('A registry for area distribution proposals.', AreaDistribution)
