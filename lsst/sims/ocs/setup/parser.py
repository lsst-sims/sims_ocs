import argparse

from lsst.sims.ocs import __version__

__all__ = ["create_parser"]

def create_parser():
    """Create the argument parser for the main driver script.
    """
    description = ["The Operations Simulator v4 is designed to operate the LSST Scheduler via"]
    description.append("the Simulated Observatory Control System (SOCS).")

    parser = argparse.ArgumentParser(usage="opsim4 [options]",
                                     description=" ".join(description),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("-c", "--startup-comment", dest="startup_comment", nargs='*',
                        default="No comment was entered.",
                        help="Enter a comment for the simulation session. NOTE: Do not use an equal sign "
                             "with the long option!")
    parser.add_argument("--frac-duration", dest="frac_duration", type=float, default=-1,
                        help="Temporary flag to set the fractional duration for the survey in units of "
                        "years.")
    parser.add_argument("--no-sched", dest="no_scheduler", action="store_true",
                        help="Flag to make program not wait for Scheduler.")
    parser.add_argument("-s", "--session-id", dest="session_id", default="1000",
                        help="Temporary flag to set a session ID.")
    parser.add_argument("--profile", dest="profile", action="store_true", help="Run the profiler on SOCS and"
                        "Scheduler code.")

    db_group_descr = ["This group of arguments controls the behavior of the simulation database."]
    db_group_descr.append("The simulation database is available through MySQL or SQLite.")
    db_group_descr.append("It is assumed that you have already setup the appropriate database using the")
    db_group_descr.append("manage_db script that came with this package.")
    db_group = parser.add_argument_group("database", " ".join(db_group_descr))
    db_group.add_argument("--db-type", dest="db_type", choices=["mysql", "sqlite"], default="mysql",
                          help="Type of database to create. MySQL assumes that a .my.cnf file is available "
                          "and contains the appropriate connection information.")

    mysql_group_descr = ["This group of arguments is for dealing with a MySQL database."]
    mysql_group = parser.add_argument_group("mysql", " ".join(mysql_group_descr))
    mysql_group.add_argument("--mysql-config-path", dest="mysql_config_path", help="For MySQL, the path to a "
                             ".my.cnf file if one is not present in $HOME.")

    sqlite_group_descr = ["This group of arguments is for dealing with a SQLite database."]
    sqlite_group = parser.add_argument_group("sqlite", " ".join(sqlite_group_descr))
    sqlite_group.add_argument("--sqlite-save-dir", dest="sqlite_save_dir", help="A directory to save the "
                              "SQLite session tracking database.")

    tracking_group_descr = ["This group of arguments controls the tracking of the simulation session."]
    track_grp = parser.add_argument_group("tracking", " ".join(tracking_group_descr))
    track_grp.add_argument("-t", "--track", dest="track_session", action="store_true",
                           help="Flag to track the current simulation in the central OpSim tracking "
                           "database.")
    track_grp.add_argument("--tracking-db", dest="tracking_db", help="Option to set an alternative URL "
                           "for the OpSim tracking database.")
    track_grp.add_argument("--session-code", dest="session_code", choices=["science", "code_dev", "system",
                           "engineering"], default="science", help="Set the type of simulation session for "
                           "the OpSim tracking database.")

    config_group_descr = ["This group of arguments controls the configuration of the simulated survey."]
    conf_grp = parser.add_argument_group("config", " ".join(config_group_descr))
    conf_grp.add_argument("--config", dest="config", nargs='*', help="Provide a set of override files for "
                          "the survey configuration. If a directory is provided, it is assumed all of the "
                          "configuration files reside there.")
    conf_grp.add_argument("--config-save-dir", dest="config_save_dir", default='',
                          help="Set a directory to save the configuration files in. The default behavior "
                          "will be to save the files in the execution directory.")
    conf_grp.add_argument("--save-config", dest="save_config", action="store_true",
                          help="Flag to save the simulation configuration.")

    log_group_descr = ["This group of arguments controls the logging of the application."]
    logging = parser.add_argument_group("logging", " ".join(log_group_descr))
    logging.add_argument("-l", "--log-path", dest="log_path", default="log",
                         help="Set the path to write log files for the application. If none, is provided, "
                         "the application will assume a directory named log in the running directory.")
    logging.add_argument("-v", "--verbose", dest="verbose", action='count', default=0,
                         help="Set the verbosity for the console and file logging. Default is to log nothing "
                         "to the console and debug to the log file. More than two levels are ignored for the "
                         "console and more than five are ignored for the log file. NOTE: Please do not use "
                         "more than three flags for long runs as it will generate LOTS of output.")

    return parser
