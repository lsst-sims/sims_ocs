import collections

__all__ = ["write_field", "write_observation_history", "write_slew_history", "write_target_history"]

def write_field(data):
    """Create a dictionary of data for the Field table.

    Parameters
    ----------
    data : SALPY_scheduler.fieldC
        The SAL target topic instance.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('ID', data.ID),
        ('fov', data.fov),
        ('ra', data.ra),
        ('dec', data.dec),
        ('gl', data.gl),
        ('gb', data.gb),
        ('el', data.el),
        ('eb', data.eb)
    ])
    return values

def write_observation_history(data, sid):
    """Create a dictionary of data for the ObsHistory table.

    Parameters
    ----------
    data : SALPY_scheduler.observationTestC
        The SAL observation topic instance.
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('observationID', data.observationId),
        ('Session_sessionID', sid),
        ('observationTime', data.observationTime),
        ('targetID', data.targetId),
        ('fieldID', data.fieldId),
        ('ra', data.ra),
        ('dec', data.dec),
        ('filter', data.filter),
        ('angle', data.angle),
        ('num_exposures', data.num_exposures)
    ])
    return values

def write_slew_history(data, sid):
    """Create a dictionary of data for the SlewHistory table.

    Parameters
    ----------
    data : class:`.SlewHistory`
        The instance containing the slew history information
    sid : int
        The current session ID. CURRENTLY UNUSED.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = data._asdict()
    return values

def write_target_history(data, sid):
    """Create a dictionary of data for the TargetHistory table.

    Parameters
    ----------
    data : SALPY_scheduler.targetTestC
        The SAL target topic instance.
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('targetID', data.targetId),
        ('Session_sessionID', sid),
        ('fieldID', data.fieldId),
        ('ra', data.ra),
        ('dec', data.dec),
        ('filter', data.filter),
        ('angle', data.angle),
        ('num_exposures', data.num_exposures)
    ])
    return values
