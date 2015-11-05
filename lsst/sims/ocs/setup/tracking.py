import logging
import os
import requests

from lsst.sims.ocs.version import __version__

class Tracking(object):
    """Main class for OpSim tracking database.

    This class is responsible for interacting with the OpSim tracking database. It collects the necessary
    information to record the simulation session to the tracking database.
    """

    def __init__(self, session_id, session_type, startup_comment):
        """

        Args:
            session_id (int): The current value of the simulation session ID.
            session_type (str): The simulation session type code.
            startup_comment (str): The startup comment with the associated simulation session.
        """
        self.session_id = session_id
        self.session_type = session_type
        self.startup_comment = startup_comment
        self.log = logging.getLogger("setup.Tracking")
        self.opsim_tracking_url = "http://opsimcvs.tuc.noao.edu/tracking"
        self.session_type_codes = {"science": 0, "code_dev": 1, "system": 2, "engineering": 3}

    @property
    def tracking_url(self):
        """The URL for the tracking call.

        Returns:
            str
        """
        return self.opsim_tracking_url + "/tracking.php"

    @property
    def update_url(self):
        """The URL for the update call."

        Returns:
            str
        """
        return self.opsim_tracking_url + "/status.php"

    def get_user(self):
        """Get the username from the environment.

        Returns:
            str
        """
        return os.getenv("USER")

    def get_hostname(self):
        """Get the hostname from the environment.

        Returns:
            str
        """
        host = os.getenv("OPSIM_HOSTNAME")
        if host is None or host == "":
            import socket
            host = socket.gethostname()
        host = host.split('.')[0]
        return host

    def get_version(self):
        """Get the version of the software.

        This function returns the version of the software. NOTE: In order to dileneate the new version of
        the Operations Simulator from version 3, a 4 is preprended to the actual software version number."

        Returns:
            (str)
        """
        return "4.{}".format(__version__)

    def track_session(self):
        """Record the simulation session into the tracking database.
        """
        payload = {'sessionID': self.session_id, 'hostname': self.get_hostname(), 'user': self.get_user(),
                   'startup_comment': self.startup_comment,
                   'code_test': self.session_type_codes[self.session_type], 'status_id': 1.0,
                   'run_version': self.get_version()}

        result = requests.get(self.tracking_url, params=payload, timeout=3.0)
        if result.ok:
            self.log.debug("Tracking for session was recorded successfully.")
        else:
            self.log.warning("Tracking for session was not recorded successfully!")
