from builtins import object
import logging
import requests

from lsst.sims.ocs.utilities import get_hostname, get_user, get_version

__all__ = ["Tracking"]

class Tracking(object):
    """Main class for OpSim tracking database.

    This class is responsible for interacting with the OpSim tracking database. It collects the necessary
    information to record the simulation session to the tracking database.

    Attributes
    ----------
    session_id : int
        The simulation session ID tag.
    session_type : str
        The simulation session type code.
    startup_comment : str
        The startup comment with the associated simulation session.
    log : logging.Logger
        The logging instance.
    opsim_tracking_url : str
        The URL for the Operations Simulator tracking database.
    session_type_codes : dict[str, int]
        The mapping of session type codes to integer values.
    """

    def __init__(self, session_id, session_type, startup_comment):
        """Initialize the class.

        Parameters
        ----------
        session_id : int
            The current value of the simulation session ID.
        session_type : str
            The simulation session type code.
        startup_comment : str
            The startup comment with the associated simulation session.
        """
        self.session_id = session_id
        self.session_type = session_type
        self.startup_comment = startup_comment
        self.log = logging.getLogger("setup.Tracking")
        self.opsim_tracking_url = "http://opsimcvs.tuc.noao.edu/tracking"
        self.session_type_codes = {"science": 0, "code_dev": 1, "system": 2, "engineering": 3}

    @property
    def tracking_url(self):
        """str: The URL for the tracking call.
        """
        return self.opsim_tracking_url + "/tracking.php"

    @property
    def update_url(self):
        """str: The URL for the update call.
        """
        return self.opsim_tracking_url + "/status.php"

    def track_session(self, hostname=None, user=None, version=None):
        """Record the simulation session into the tracking database.

        Parameters
        ----------
        hostname : str, optional
            An alternate hostname.
        user : str, optional
            An alternate username.
        version : str, optional
            An alternate version number.
        """
        if hostname is None:
            hostname = get_hostname()

        if user is None:
            user = get_user()

        if version is None:
            version = get_version()

        payload = {'sessionID': self.session_id, 'hostname': hostname, 'user': user,
                   'startup_comment': self.startup_comment,
                   'code_test': self.session_type_codes[self.session_type], 'status_id': 1.0,
                   'run_version': version}

        result = requests.get(self.tracking_url, params=payload, timeout=3.0)
        if result.ok:
            self.log.debug("Tracking for session was recorded successfully.")
        else:
            self.log.warning("Tracking for session was not recorded successfully!")

    def update_session(self, eng_comment, hostname=None):
        """Update the simulation session in the tracking database with a comment.

        This function allows the simulation session's entry in the tracking database to be updated with an
        engineering comment. This is hopefully to record that the simulation has completed successfully, but
        may be used to indicate a simulation failure.

        Parameters
        ----------
        eng_comment : str
            A comment about the simulation session hopefully for a successful run.
        hostname : str, optional
            An alternate hostname
        """
        if hostname is None:
            hostname = get_hostname()

        payload = {'sessionID': self.session_id, 'hostname': hostname, 'eng_comment': eng_comment}

        result = requests.get(self.update_url, params=payload, timeout=3.0)
        if result.ok:
            self.log.debug("Update for session was recorded successfully.")
        else:
            self.log.warning("Update for session was not recorded successfully!")
