import importlib
import os
import sys

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import load_config
from lsst.sims.ocs.configuration.proposal import general_prop_reg, sequence_prop_reg
from lsst.sims.ocs.utilities.socs_exceptions import NoProposalsConfiguredError

__all__ = ["ScienceProposals"]

class ScienceProposals(pexConfig.Config):
    """Configuration for the science proposals.
    """

    general_props = general_prop_reg.makeField('The list of general proposals.', optional=True, multi=True)
    sequence_props = sequence_prop_reg.makeField('The list of sequence proposals.', optional=True, multi=True)

    @property
    def general_proposals(self):
        """Listing of available general proposals.

        Returns
        -------
        list[str]
           The available general proposals.
        """
        return sorted(self.general_props.registry.keys())

    @property
    def sequence_proposals(self):
        """Listing of available sequence proposals.

        Returns
        -------
        list[str]
           The available sequence proposals.
        """
        return sorted(self.sequence_props.registry.keys())

    def load(self, config_files):
        """Load the configuration override files.

        Parameters
        ----------
        config_files : list[str]
            A set of configuration override files.
        """
        for prop in self.general_props.values():
            load_config(prop, config_files)
        for prop in self.sequence_props.values():
            load_config(prop, config_files)

    def load_proposals(self, proposals, alternate_proposals=None):
        """Load given proposals.

        This function loads the propsals requested from the function argument.
        The argument is a dictionary with two keys: GEN or SEQ and a comma-delimited
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
        proposal_related = ['General', 'BandFilter', 'SELECTION_LIMIT_TYPES', 'Selection',
                            'Sequence', 'general_prop_reg', 'sequence_prop_reg', 'pexConfig',
                            'SelectionList', 'TimeRange', 'GeneralBandFilter', 'SubSequence',
                            'MasterSubSequence', 'BaseSequence']
        if alternate_proposals is not None:
            sys.path.append(alternate_proposals)
            prop_files = os.listdir(alternate_proposals)
            for prop_file in prop_files:
                if not prop_file.endswith(".py"):
                    continue
                prop_mod = prop_file.split('.')[0]
                module = importlib.import_module(prop_mod)
                all_names = [x for x in dir(module) if not x.startswith("__")]
                if "General" in all_names:
                    key = "GEN"
                if "Sequence" in all_names:
                    key = "SEQ"
                prop_name = [x for x in all_names if x not in proposal_related][0]
                if len(proposals[key]):
                    proposals[key].append(prop_name)
                else:
                    proposals[key] = [prop_name]

        if len(proposals["GEN"]):
            self.general_props.names = proposals["GEN"]
        if len(proposals["SEQ"]):
            self.sequence_props.names = proposals["SEQ"]

        if not len(proposals["GEN"]) and not len(proposals["SEQ"]):
            raise NoProposalsConfiguredError("Please run at least one science proposal!")

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
        for prop_name, prop in self.sequence_props.items():
            if prop_name in self.sequence_props.names:
                prop.save(os.path.join(save_dir, prop_name.lower() + "_prop.py"))
