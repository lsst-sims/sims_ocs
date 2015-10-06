from enum import Enum
import logging

class VerboseLevel(Enum):
    """Handle the verbosity level in the code.
    """
    quiet = 0
    minimal = 1
    wordy = 2
    verbose = 3
    noisy = 4

class DebugLevel(Enum):
    """Handle the debugging level in the code.
    """
    minimal = 0
    diagnostic = 1
    extensive = 2
    trace = 3

def configure_logging(log_file_path="log", session_id="1000"):
    """Configure logging for the application.

    Configuration for both the console and file logging for the application.

    Args:
        log_file_path: A string containing the location to write the log file.
        session_id: A string containing the OpSim session ID tag.
    """
    import os
    if not os.path.exists(log_file_path):
        log_file_path = ""
    log_file = os.path.join(log_file_path, "lsst.log_{}".format(session_id))

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        filename=log_file,
                        filemode="w")

    console_format = logging.Formatter('%(name)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(console_format)

    logging.getLogger('').addHandler(ch)
