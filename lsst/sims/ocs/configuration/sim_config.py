import os

import lsst.pex.config as pexConfig

from .lsst_survey import LsstSurvey
from .obs_site import ObservingSite

__all__ = ["SimulationConfig"]

class SimulationConfig(pexConfig.Config):
    """Configuration for the survey simulation.

       This class gathers all of the configuration objects into one place.
    """
    lsst_survey = pexConfig.ConfigField("The configuration for the LSST survey.", LsstSurvey)
    observing_site = pexConfig.ConfigField("The observing site configuration.", ObservingSite)

    def setDefaults(self):
        """Set the defaults survey simulation.
        """
        pass

    def load(self, ifiles):
        """Load and apply configuration override files.

        This function loads the specified configuration files and applies them to the configuration
        objects. If input is a directory, it is assumed that all files in that directory are override
        files.

        Args:
            ifiles: A list of files or a directory containing configuration overrides.
        """
        if ifiles is None:
            return
        config_files = []
        for ifile in ifiles:
            if os.path.isdir(ifile):
                dfiles = os.listdir(ifile)
                for dfile in dfiles:
                    full_dfile = os.path.join(ifile, dfile)
                    if os.path.isfile(full_dfile):
                        config_files.append(full_dfile)
            else:
                config_files.append(ifile)

        if len(config_files):
            self._load_config(self.lsst_survey, config_files)
            self._load_config(self.observing_site, config_files)

    def _load_config(self, config_obj, ifiles):
        """Apply override file to configuration object.

        This function does the actual work of going through the override files and applying the
        correct one to the given configuration object.

        Args:
            config_obj: The configuration object to apply overrides.
            ifiles: The list of overriding configuration files.
        """
        for ifile in ifiles:
            try:
                config_obj.load(ifile)
            except AssertionError:
                # Not the right configuration file, so do nothing.
                pass

    def save(self, save_dir=''):
        """Save the configuration objects to files.

        This function saves the configuration objects to separate files.

        Args:
            save_dir: A string containing the directory in which to save the configuration files.
        """
        self.lsst_survey.save(os.path.join(save_dir, "lsst_survey_config.py"))
        self.observing_site.save(os.path.join(save_dir, "observing_site_config.py"))
