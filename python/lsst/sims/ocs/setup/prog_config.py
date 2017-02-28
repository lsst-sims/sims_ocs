try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os

from lsst.sims.ocs.utilities import expand_path

__all__ = ["apply_file_config", "read_file_config", "write_file_config"]

def apply_file_config(config, options):
    """Apply configuration file values to the command-line options.

    Parameters
    ----------
    config : configparser.ConfigParser
        The configuration file instance.
    options : argparse.Namespace
        The command-line options instance.
    """
    # When the code switches to Python 3 for good, replace the get calls with dictionary access
    # and change the exceptions from configparser.NoOptionError configparser.NoSectionError to KeyError.
    options.db_type = config.get("Database", "type")
    try:
        options.sqlite_save_dir = config.get(options.db_type, "save_directory")
    except configparser.NoOptionError:
        pass
    try:
        options.sqlite_session_save_dir = config.get(options.db_type, "session_save_directory")
    except configparser.NoOptionError:
        pass
    try:
        options.session_id_start = int(config.get(options.db_type, "session_id_start"))
    except configparser.NoOptionError:
        pass
    try:
        options.track_session = config.has_section("tracking")
    except configparser.NoSectionError:
        pass
    try:
        options.tracking_db = config.get("tracking", "tracking_db")
    except (configparser.NoOptionError, configparser.NoSectionError):
        pass

def write_file_config(options, conf_dir=None):
    """Write a configuration file from the given options.

    Parameters
    ----------
    options : argparse.Namespace
        The options from ArgumentParser
    conf_dir : str, optional
        A directory for saving the configuration file in. Default is $HOME/.config/opsim4.
    """
    parser = configparser.SafeConfigParser()

    parser.add_section("Database")
    parser.set("Database", "type", options.type)
    parser.add_section(options.type)
    parser.set(options.type, "save_directory", options.save_dir)
    if options.session_save_dir is not None:
        parser.set(options.type, "session_save_directory", options.session_save_dir)
    if options.session_id_start is not None:
        parser.set(options.type, "session_id_start", options.session_id_start)

    if conf_dir is None:
        conf_dir = expand_path(os.path.join("$HOME", ".config"))
    with open(os.path.join(conf_dir, "opsim4"), 'w') as cfile:
        parser.write(cfile)

def read_file_config(conf_file=None, conf_dir=None):
    """Read in a configuration file.

    Parameters
    ----------
    conf_file : str, optional
        The name of the configuration file. Default is opsim4.
    conf_dir : str, optional
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
