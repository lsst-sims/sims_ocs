import importlib
import os
import sys

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import load_config
from lsst.sims.ocs.configuration.proposal import general_prop_reg

__all__ = ["ScienceProposals"]

class ScienceProposals(pexConfig.Config):
    """Configuration for the science propsals.
    """

    general_props = general_prop_reg.makeField('The list of general proposals.', multi=True)

    @property
    def general_proposals(self):
        """Listing of available general proposals.

        Returns
        -------
        list[str]
           The available general proposals.
        """
        return sorted(self.general_props.registry.keys())

    def load(self, config_files):
        """Load the configuration override files.

        Parameters
        ----------
        config_files : list[str]
            A set of configuration override files.
        """
        for prop in self.general_props.values():
            load_config(prop, config_files)

    def load_proposals(self, proposals, alternate_proposals=None):
        """Load given proposals.

        This function loads the propsals requested from the function argument.
        The argument is a dictionary with two keys: GEN or SS and a comma-delimited
        list of proposal names associated with each key.

        Parameters
        ----------
        proposals : dict[str: list[str]]
            The set of proposals to load.
        alternate_proposals : str
            A directory location containing alternate proposals to load.
        """
        # Listing of all the things related to a proposal but not including the
        # actual class name,
        proposal_related = ['General', 'BandFilter', 'SELECTION_LIMIT_TYPES',
                            'Selection', 'general_prop_reg', 'pexConfig']
        if alternate_proposals is not None:
            sys.path.append(alternate_proposals)
            prop_files = os.listdir(alternate_proposals)
            for prop_file in prop_files:
                if ".pyc" in prop_file:
                    continue
                prop_mod = prop_file.split('.')[0]
                module = importlib.import_module(prop_mod)
                all_names = [x for x in dir(module) if not x.startswith("__")]
                if "General" in all_names:
                    key = "GEN"
                prop_name = [x for x in all_names if x not in proposal_related][0]
                if len(proposals[key]):
                    proposals[key].append(prop_name)
                else:
                    proposals[key] = [prop_name]

        if len(proposals["GEN"]):
            self.general_props.names = proposals["GEN"]

    def save_as(self, save_dir=''):
        """Save the configuration objects to separate files.

        Parameters
        ----------
        save_dir : str
            The directory in which to save the configuration files.
        """
        for prop_name, prop in self.general_props.items():
            if prop_name in self.general_props.names:
                prop.save(os.path.join(save_dir, prop_name.lower() + "_prop.py"))
