from enum import Enum
import logging
import os

__all__ = ["LoggingLevel", "configure_logging"]

MAX_VERBOSE = 2
MAX_DEBUG = 2

class LoggingLevel(Enum):
    """Handle some extra logging levels.
    """
    # Extra INFO levels
    WORDY = 15
    # Extra DEBUG levels
    EXTENSIVE = 5
    TRACE = 2

VERBOSE_LEVEL = {
    0: logging.WARN,
    1: logging.INFO,
    2: LoggingLevel.WORDY.value
}

DEBUG_LEVEL = {
    0: logging.DEBUG,
    1: LoggingLevel.EXTENSIVE.value,
    2: LoggingLevel.TRACE.value
}

def configure_logging(log_file_path="log", session_id="1000", verbose=0, debug=0):
    """Configure logging for the application.

    Configuration for both the console and file logging for the application.

    Parameters
    ----------
    log_file_path : Optional[str]
        The location to write the log file.
    session_id : Optional[str]
        The OpSim session ID tag.
    verbose : Optional[int]
        The INFO logging level.
    debug : Optional[int]
        The DEBUG logging level.
    """

    max_verbose = max(VERBOSE_LEVEL.keys())
    max_debug = max(DEBUG_LEVEL.keys())

    if verbose > max_verbose:
        verbose = max_verbose

    if debug > max_debug:
        debug = max_debug

    if not os.path.exists(log_file_path):
        log_file_path = ""
    log_file = os.path.join(log_file_path, "lsst.log_{}".format(session_id))

    logging.basicConfig(level=DEBUG_LEVEL[debug],
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        filename=log_file,
                        filemode="w")

    for level in LoggingLevel:
        logging.addLevelName(level.value, level.name)

    console_format = logging.Formatter('%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(VERBOSE_LEVEL[verbose])
    ch.setFormatter(console_format)

    logging.getLogger('').addHandler(ch)
