import os.path

def expand_path(input_path):
    """Replace ~/ and environmental variables in path.

    Parameters
    ----------
    input_path : str
        The path to possible replace special portions.

    Returns
    -------
    str
        The path with special portions expanded.
    """
    return os.path.expanduser(os.path.expandvars(input_path))
