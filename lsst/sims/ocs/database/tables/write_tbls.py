import collections

__all__ = ["write_field", "write_observation_exposures", "write_observation_history", "write_slew_history",
           "write_target_exposures", "write_target_history"]

def ordered_dict_from_namedtuple(data, sid=None):
    """Convert a namedtuple to an OrderedDict.

    Parameters
    ----------
    data : collections.namedtuple
        The data to convert.
    sid : int (Optional)
        The current session ID.

    Returns
    -------
        collections.OrderedDict
    """
    values = data._asdict()
    if sid is not None:
        values["Session_sessionId"] = sid
    return values

def write_field(data, sid):
    """Create a dictionary of data for the Field table.

    Parameters
    ----------
    data : SALPY_scheduler.fieldC
        The SAL target topic instance.
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('fieldId', data.ID),
        ('Session_sessionId', sid),
        ('fov', data.fov),
        ('ra', data.ra),
        ('dec', data.dec),
        ('gl', data.gl),
        ('gb', data.gb),
        ('el', data.el),
        ('eb', data.eb)
    ])
    return values

def write_observation_exposures(data, sid):
    """Create a dictionary of data for the ObsExposures table.

    Parameters
    ----------
    data : class:`.ObsExposure`
        The instance containing the observation exposure information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

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
        ('observationId', data.observationId),
        ('Session_sessionId', sid),
        ('observationStartTime', data.observationTime),
        ('TargetHistory_targetId', data.targetId),
        ('Field_fieldId', data.fieldId),
        ('ra', data.ra),
        ('dec', data.dec),
        ('filter', data.filter),
        ('angle', data.angle),
        ('numExposures', data.num_exposures),
        ('visitTime', data.visit_time),
        ('visitExposureTime', sum([data.exposure_times[i] for i in range(data.num_exposures)]))
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

def write_target_exposures(data, sid):
    """Create a dictionary of data for the TargetExposures table.

    Parameters
    ----------
    data : class:`.TargetExposure`
        The instance containing the target exposure information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

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
        ('targetId', data.targetId),
        ('Session_sessionId', sid),
        ('Field_fieldId', data.fieldId),
        ('ra', data.ra),
        ('dec', data.dec),
        ('filter', data.filter),
        ('angle', data.angle),
        ('numExposures', data.num_exposures),
        ('requestedExpTime', sum([data.exposure_times[i] for i in range(data.num_exposures)]))
    ])
    return values
