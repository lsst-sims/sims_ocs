try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os

from ..utilities.file_helpers import expand_path

__all__ = ["read_file_config", "write_file_config"]

def write_file_config(options, conf_dir=None):
    """Write a configuration file from the given options.

    Parameters
    ----------
    options : argparse.Namespace
        The options from ArgumentParser
    conf_dir : Optional[str]
        A directory for saving the configuration file in. Default is $HOME/.config/opsim4.
    """
    parser = configparser.SafeConfigParser()

    parser.add_section("Database")
    parser.set("Database", "type", options.type)
    parser.add_section(options.type)
    if options.type == "sqlite":
        parser.set(options.type, "save_directory", options.save_dir)
    if options.type == "mysql" and options.config_path is not None:
        parser.set(options.type, "config_path", options.config_path)

    if conf_dir is None:
        conf_dir = expand_path(os.path.join("$HOME", ".config"))
    with open(os.path.join(conf_dir, "opsim4"), 'w') as cfile:
        parser.write(cfile)

def read_file_config(conf_file=None, conf_dir=None):
    """Read in a configuration file.

    Parameters
    ----------
    conf_file : Optional[str]
        The name of the configuration file. Default is opsim4.
    conf_dir : Optional[str]
        The directory location of the configuration file. Default is $HOME/.config
    """
    if conf_file is None:
        conf_file = "opsim4"
    if conf_dir is None:
        conf_dir = expand_path(os.path.join("$HOME", ".config"))

    full_conf_file = os.path.join(conf_dir, conf_file)
    if not os.path.exists(full_conf_file):
        return None

    parser = configparser.SafeConfigParser()
    parser.read(full_conf_file)
    return parser
