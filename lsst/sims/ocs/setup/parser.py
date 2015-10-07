import argparse

from lsst.sims.ocs.version import __version__

def create_parser():
    """Create the argument parser for the main driver script.
    """
    description = ["The Operations Simulator v4 is designed to operate the LSST Scheduler via"]
    description.append("the Simulated Observatory Control System (SOCS).")

    parser = argparse.ArgumentParser(usage="opsim4 [options]",
                                     description=" ".join(description),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--version", action="version", version=__version__)

    parser.add_argument("--frac-duration", dest="frac_duration", type=float, default=1.0 / 365.0,
                        help="Temporary flag to set the fractional duration for the survey in units of "
                        "years.")

    log_group_descr = ["This group of arguments controls the logging of the application."]
    logging = parser.add_argument_group("logging", " ".join(log_group_descr))
    logging.add_argument("-l", "--log-path", dest="log_path", default="log",
                         help="Set the path to write log files for the application. If none, is provided, "
                         "the application will assume a directory named log in the running directory.")
    logging.add_argument("-v", "--verbose", dest="verbose", action='count', default=0,
                         help="Set the verbosity for the console logging. These messages will also be "
                         "written to the log file at the same verbosity level. More than four verbose flags "
                         "are ignored.")
    logging.add_argument("-d", "--debug", dest="debug", action='count', default=0,
                         help="Set the debugging level for the log file. CAUTION: Do not use more than two "
                         "debug flags on simulations over three days. More than three debug flags are "
                         "ignored.")

    return parser
