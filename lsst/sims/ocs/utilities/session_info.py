import os

from lsst.sims.ocs import __version__

__all__ = ["get_hostname", "get_user", "get_version"]

def get_user():
    """Get the username from the environment.

    Returns
    -------
    str
        The usename of the simulation runner.
    """
    return os.getenv("USER")

def get_hostname():
    """Get the hostname from the environment.

    Returns
    -------
    str
        The hostname of the simulation running computer.
    """
    host = os.getenv("OPSIM_HOSTNAME")
    if host is None or host == "":
        import socket
        host = socket.gethostname()
    host = host.split('.')[0]
    return host

def get_version():
    """Get the version of the software.

    This function returns the version of the software.

    Note
    ----
    In order to delineate the new version of the Operations Simulator from version 3, a 4 is
    prepended to the actual software version number.

    Returns
    -------
    str
        The version number for the simulation software.
    """
    return "4.{}".format(__version__)
