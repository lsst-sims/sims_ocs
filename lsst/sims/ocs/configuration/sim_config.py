import os

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import Downtime, Environment, load_config, Observatory, ObservingSite
from lsst.sims.ocs.configuration import SchedulerDriver, ScienceProposals, Survey
from lsst.sims.ocs.utilities import expand_path

__all__ = ["SimulationConfig"]

class SimulationConfig(pexConfig.Config):
    """Configuration for the survey simulation.

    This class gathers all of the configuration objects into one place.
    """
    survey = pexConfig.ConfigField("The LSST survey configuration.", Survey)
    science = pexConfig.ConfigField("The science proposal configuration.", ScienceProposals)
    observing_site = pexConfig.ConfigField("The observing site configuration.", ObservingSite)
    observatory = pexConfig.ConfigField("The LSST observatory configuration.", Observatory)
    downtime = pexConfig.ConfigField("The LSST downtime configuration.", Downtime)
    sched_driver = pexConfig.ConfigField("The LSST Scheduler driver configuration.", SchedulerDriver)
    environment = pexConfig.ConfigField("The environmental configuration.", Environment)

    def setDefaults(self):
        """Set defaults for the survey simulation.
        """
        pass

    @property
    def num_proposals(self):
        """The total number of active proposals.

        Returns
        -------
        int
        """
        num_props = 0
        if self.science.area_dist_props.names is not None:
            num_props += len(self.science.area_dist_props.names)
        return num_props

    def load(self, ifiles):
        """Load and apply configuration override files.

        This function loads the specified configuration files and applies them to the configuration
        objects. If input is a directory, it is assumed that all files in that directory are override
        files.

        Parameters
        ----------
        ifiles : list[str]
            A list of files or directories containing configuration overrides.
        """
        if ifiles is None:
            return
        config_files = []
        for ifile in ifiles:
            ifile = expand_path(ifile)
            if os.path.isdir(ifile):
                dfiles = os.listdir(ifile)
                for dfile in dfiles:
                    full_dfile = os.path.join(ifile, dfile)
                    if os.path.isfile(full_dfile):
                        config_files.append(full_dfile)
                    if os.path.isdir(full_dfile):
                        self.survey.alt_proposal_dir = full_dfile
            else:
                config_files.append(ifile)

        if len(config_files):
            load_config(self.survey, config_files)
            self.science.load(config_files)
            load_config(self.observing_site, config_files)
            self.observatory.load(config_files)
            load_config(self.downtime, config_files)
            load_config(self.sched_driver, config_files)
            load_config(self.environment, config_files)

    def load_proposals(self):
        """Tell the science proposals to load their configuration.
        """
        self.science.load_proposals({"AD": self.survey.ad_proposals},
                                    alternate_proposals=self.survey.alt_proposal_dir)

    def save(self, save_dir=''):
        """Save the configuration objects to separate files.

        Parameters
        ----------
        save_dir : str
            The directory in which to save the configuration files.
        """
        self.survey.save(os.path.join(save_dir, "survey.py"))
        self.science.save_as(save_dir)
        self.observing_site.save(os.path.join(save_dir, "observing_site.py"))
        self.observatory.save_as(save_dir)
        self.downtime.save(os.path.join(save_dir, "downtime.py"))
        self.sched_driver.save(os.path.join(save_dir, "sched_driver.py"))
        self.environment.save(os.path.join(save_dir, "environment.py"))
