import os

from ..version import __version__

def get_user():
    """Get the username from the environment.

    Returns:
        str
    """
    return os.getenv("USER")

def get_hostname():
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

def get_version():
    """Get the version of the software.

    This function returns the version of the software. NOTE: In order to delineate the new version of
    the Operations Simulator from version 3, a 4 is prepended to the actual software version number."

    Returns:
        (str)
    """
    return "4.{}".format(__version__)
