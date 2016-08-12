import collections

__all__ = ["write_field", "write_observation_exposures", "write_observation_history", "write_proposal",
           "write_proposal_history", "write_scheduled_downtime", "write_slew_activities",
           "write_slew_history",
           "write_slew_final_state", "write_slew_initial_state", "write_slew_maxspeeds",
           "write_target_exposures", "write_target_history", "write_unscheduled_downtime"]

def ordered_dict_from_namedtuple(data, sid=None):
    """Convert a namedtuple to an OrderedDict.

    Parameters
    ----------
    data : collections.namedtuple
        The data to convert.
    sid : int, optional
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
    data : tuple
        The set of information from a field.
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('fieldId', data[0]),
        ('Session_sessionId', sid),
        ('fov', data[1]),
        ('ra', data[2]),
        ('dec', data[3]),
        ('gl', data[4]),
        ('gb', data[5]),
        ('el', data[6]),
        ('eb', data[7])
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
        ('observationStartTime', data.observation_start_time),
        ('observationStartMJD', data.observation_start_mjd),
        ('observationStartLST', data.observation_start_lst),
        ('night', data.night),
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

def write_proposal(data, sid):
    """Create a dictionary of data for the Proposal table.

    Parameters
    ----------
    data : tuple
        The instance containing the proposal information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_proposal_history(data, sid):
    """Create a dictionary of data for the ProposalHistory table.

    Parameters
    ----------
    data : tuple
        The instance containing the proposal history information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_scheduled_downtime(data, sid):
    """Create a dictionary of data for the ScheduledDowntime table.

    Parameters
    ----------
    data : tuple
        The instance containing the scheduled downtime information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('night', data[0]),
        ('Session_sessionId', sid),
        ('duration', data[1]),
        ('activity', data[2])
    ])
    return values

def write_slew_activities(data, sid):
    """Create a dictionary of data for the SlewHistory table.

    Parameters
    ----------
    data : class:`.SlewActivity`
        The instance containing the slew activity information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_slew_history(data, sid):
    """Create a dictionary of data for the SlewHistory table.

    Parameters
    ----------
    data : class:`.SlewHistory`
        The instance containing the slew history information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_slew_final_state(data, sid):
    """Create a dictionary of data for the SlewFinalState table.

    Parameters
    ----------
    data : class:`.SlewFinalState`
        The instance containing the slew state information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_slew_initial_state(data, sid):
    """Create a dictionary of data for the SlewInitialState table.

    Parameters
    ----------
    data : class:`.SlewInitialState`
        The instance containing the slew state information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_slew_maxspeeds(data, sid):
    """Create a dictionary of data for the SlewMaxSpeeds table.

    Parameters
    ----------
    data : class:`.SlewMaxSpeeds`
        The instance containing the slew maxspeeds information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

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
        ('requestedExpTime', sum([data.exposure_times[i] for i in range(data.num_exposures)])),
        ('requestTime', data.request_time),
        ('airmass', data.airmass),
        ('skyBrightness', data.sky_brightness),
        ('slewTime', data.slew_time),
        ('costBonus', data.cost_bonus),
        ('rank', data.rank),
        ('numRequestingProps', data.num_proposals),
        ('moonRA', data.moon_ra),
        ('moonDec', data.moon_dec),
        ('moonAlt', data.moon_alt),
        ('moonAz', data.moon_az),
        ('moonDistance', data.moon_distance),
        ('moonPhase', data.moon_phase),
        ('sunRA', data.sun_ra),
        ('sunDec', data.sun_dec),
        ('sunAlt', data.sun_alt),
        ('sunAz', data.sun_az),
        ('sunElong', data.sun_elong)
    ])
    return values

def write_unscheduled_downtime(data, sid):
    """Create a dictionary of data for the UnscheduledDowntime table.

    Parameters
    ----------
    data : tuple
        The instance containing the unscheduled downtime information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    values = collections.OrderedDict([
        ('night', data[0]),
        ('Session_sessionId', sid),
        ('duration', data[1]),
        ('activity', data[2])
    ])
    return values
