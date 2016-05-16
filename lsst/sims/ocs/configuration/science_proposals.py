import collections
import importlib
import os

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import load_config
from lsst.sims.ocs.configuration.proposal import area_dist_prop_reg, load_class
from lsst.sims.ocs.configuration.proposal import AreaDistribution

__all__ = ["ScienceProposals"]

class ScienceProposals(pexConfig.Config):
    """Configuration for the science propsals.
    """

    area_dist_props = area_dist_prop_reg.makeField('The list of area distribution proposals.', multi=True)

    def load(self, config_files):
        """Load the configuration override files.

        Parameters
        ----------
        config_files : list[str]
            A set of configuration override files.
        """
        for prop in self.area_dist_props.values():
            load_config(prop, config_files)

    def load_proposals(self):
        """Load proposals from configuration.science module.
        """

        AREA_DIST = "AreaDistribution"
        proposal_dict = collections.defaultdict(list)

        proposal_module = "lsst.sims.ocs.configuration.science"
        module = importlib.import_module(proposal_module)
        names = dir(module)
        for name in names:
            cls = load_class(proposal_module + "." + name)
            try:
                key = None
                if issubclass(cls, AreaDistribution):
                    key = AREA_DIST
                if key is not None:
                    proposal_dict[key].append(cls.__name__)
            except TypeError:
                # Don't care about things that aren't classes.
                pass

        self.area_dist_props.names = proposal_dict[AREA_DIST]

    def save_as(self, save_dir=''):
        """Save the configuration objects to separate files.

        Parameters
        ----------
        save_dir : str
            The directory in which to save the configuration files.
        """
        for prop_name, prop in self.area_dist_props.items():
            prop.save(os.path.join(save_dir, prop_name.lower() + "_prop.py"))
