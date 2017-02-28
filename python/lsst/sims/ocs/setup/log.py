from enum import Enum
import logging
import logging.handlers
import os

from lsst.sims.ocs.utilities import get_hostname

__all__ = ["LoggingLevel", "configure_logging", "generate_logfile_path", "set_log_levels"]

MAX_CONSOLE = 2
MIN_FILE = 3
MAX_FILE = 5

CONSOLE_FORMAT = "%(message)s"

class LoggingLevel(Enum):
    """Handle some extra logging levels.
    """
    # Extra INFO levels
    WORDY = 15
    # Extra DEBUG levels
    EXTENSIVE = 5
    TRACE = 2

DETAIL_LEVEL = {
    0: logging.ERROR,
    1: logging.INFO,
    2: LoggingLevel.WORDY.value,
    3: logging.DEBUG,
    4: LoggingLevel.EXTENSIVE.value,
    5: LoggingLevel.TRACE.value
}

def configure_logging(console_detail, file_detail, log_port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
    """Configure logging for the application.

    Configuration for both the console and file (via socket) logging for the application.

    Parameters
    ----------
    console_detail : int
        The requested detail level for the console logger.
    file_detail : int
        The requested detail level for the socket (file) logger.
    log_port : int, optional
        An alternate port for the socker logger.
    """
    main_level = max(console_detail, file_detail)
    logging.basicConfig(level=DETAIL_LEVEL[main_level], format=CONSOLE_FORMAT)
    logging.captureWarnings(True)
    # Remove old console logger as it will double up messages when levels match.
    logging.getLogger().removeHandler(logging.getLogger().handlers[0])

    for level in LoggingLevel:
        logging.addLevelName(level.value, level.name)

    ch = logging.StreamHandler()
    ch.setLevel(DETAIL_LEVEL[console_detail])
    ch.setFormatter(logging.Formatter(CONSOLE_FORMAT))
    logging.getLogger().addHandler(ch)

    sh = logging.handlers.SocketHandler('localhost', log_port)
    logging.getLogger().addHandler(sh)

def set_log_levels(verbose=0):
    """Set detail levels for console and file logging systems.

    This function sets the detail levels for console and file (via socket) logging systems. These
    levels are keys into the DETAIL_LEVEL dictionary.

    Parameters
    ----------
    verbose : int
        The requested verbosity level.

    Returns
    -------
    (int, int)
        A tuple containing the console detail level and the file detail level respectively.
    """
    console_detail = MAX_CONSOLE if verbose > MAX_CONSOLE else verbose

    file_detail = MIN_FILE if verbose < MIN_FILE else verbose
    file_detail = MAX_FILE if file_detail > MAX_FILE else file_detail

    return (console_detail, file_detail)

def generate_logfile_path(log_file_path="log", session_id="1000"):
    """Generate the full log file path.

    Parameters
    ----------
    log_file_path : str, optional
        The location to write the log file.
    session_id : str, optional
        The OpSim session ID tag.

    Returns
    -------
    str
        The full path of the log file.
    """
    if not os.path.exists(log_file_path):
        log_file_path = ""
    log_file = os.path.join(log_file_path, "{}_{}.log".format(get_hostname(), session_id))
    return log_file
