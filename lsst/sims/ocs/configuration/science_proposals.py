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

    @property
    def ad_proposals(self):
        """Listing of available area distribution proposals.

        Returns
        -------
        str
            Comma-delimited list of available area distribution proposals.
        """
        return ",".join(sorted(self.area_dist_props.registry.keys()))

    def load(self, config_files):
        """Load the configuration override files.

        Parameters
        ----------
        config_files : list[str]
            A set of configuration override files.
        """
        for prop in self.area_dist_props.values():
            load_config(prop, config_files)

    def load_proposals(self, proposals):
        """Load given proposals.

        This function loads the propsals requested from the function argument.
        The argument is a dictionary with two keys: AD or TD and a comma-delimited
        list of proposal names associated with each key.

        Parameters
        ----------
        proposals : dict[str: str]
            The set of proposals to load.
        """

        # AREA_DIST = "AreaDistribution"
        # proposal_dict = collections.defaultdict(list)

        # proposal_module = "lsst.sims.ocs.configuration.science"
        # module = importlib.import_module(proposal_module)
        # names = dir(module)
        # for name in names:
        #     cls = load_class(proposal_module + "." + name)
        #     try:
        #         key = None
        #         if issubclass(cls, AreaDistribution):
        #             key = AREA_DIST
        #         if key is not None:
        #             proposal_dict[key].append(cls.__name__)
        #     except TypeError:
        #         # Don't care about things that aren't classes.
        #         pass

        # self.area_dist_props.names = proposal_dict[AREA_DIST]
        if proposals["AD"] != "":
            self.area_dist_props.names = [prop for prop in proposals["AD"].split(',')]

    def save_as(self, save_dir=''):
        """Save the configuration objects to separate files.

        Parameters
        ----------
        save_dir : str
            The directory in which to save the configuration files.
        """
        for prop_name, prop in self.area_dist_props.items():
            if prop_name in self.area_dist_props.names:
                prop.save(os.path.join(save_dir, prop_name.lower() + "_prop.py"))
