from builtins import range
import collections

__all__ = ["write_config", "write_field", "write_observation_exposures",
           "write_observation_history", "write_observation_proposal_history", "write_proposal_field",
           "write_proposal", "write_scheduled_downtime",
           "write_slew_activities", "write_slew_history",
           "write_slew_final_state", "write_slew_initial_state", "write_slew_maxspeeds",
           "write_target_exposures", "write_target_history", "write_target_proposal_history",
           "write_unscheduled_downtime"]

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

def write_config(data, sid):
    """Create a dictionary of data for the Config table.

    Parameters
    ----------
    data : tuple
        The set of information from a configuration parameter.
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the data.
    """
    values = collections.OrderedDict([
        ('configId', data[0]),
        ('Session_sessionId', sid),
        ('paramName', data[1]),
        ('paramValue', data[2])
    ])

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
    data : SALPY_scheduler.observationC
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
        ('observationStartTime', data.observationStartTime),
        ('observationStartMJD', data.observationStartMjd),
        ('observationStartLST', data.observationStartLst),
        ('night', data.night),
        ('TargetHistory_targetId', data.targetId),
        ('Field_fieldId', -1),
        ('groupId', data.groupId),
        ('ra', data.ra),
        ('dec', data.decl),
        ('filter', data.filter),
        ('angle', data.angle),
        ('altitude', data.altitude),
        ('azimuth', data.azimuth),
        ('numExposures', data.numExposures),
        ('visitTime', data.visitTime),
        ('visitExposureTime', sum([data.exposureTimes[i] for i in range(data.numExposures)])),
        ('airmass', data.airmass),
        ('skyBrightness', data.skyBrightness),
        ('cloud', data.cloud),
        ('seeingFwhm500', data.seeingFwhm500),
        ('seeingFwhmGeom', data.seeingFwhmGeom),
        ('seeingFwhmEff', data.seeingFwhmEff),
        ('fiveSigmaDepth', data.fiveSigmaDepth),
        ('moonRA', data.moonRa),
        ('moonDec', data.moonDec),
        ('moonAlt', data.moonAlt),
        ('moonAz', data.moonAz),
        ('moonDistance', data.moonDistance),
        ('moonPhase', data.moonPhase),
        ('sunRA', data.sunRa),
        ('sunDec', data.sunDec),
        ('sunAlt', data.sunAlt),
        ('sunAz', data.sunAz),
        ('solarElong', data.solarElong),
        ('slew_time', data.slewTime),
        ('note', data.note)
    ])
    return values

def write_observation_proposal_history(data, sid):
    """Create a dictionary of data for the ObsProposalHistory table.

    Parameters
    ----------
    data : tuple
        The instance containing the observation proposal history information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

def write_proposal_field(data, sid):
    """Create a dictionary of data for the ProposalField table.

    Parameters
    ----------
    data : tuple
        The instance containing the proposal field information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

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
    data : SALPY_scheduler.targetC
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
        ('Field_fieldId', -1),
        ('groupId', -1),
        ('ra', data.ra),
        ('dec', data.decl),
        ('filter', data.filter),
        ('angle', data.skyAngle),
        ('numExposures', data.numExposures),
        ('requestedExpTime', sum([data.exposureTimes[i] for i in range(data.numExposures)])),
        ('requestTime', data.requestTime),
        ('requestMJD', data.requestMjd),
        ('airmass', data.airmass),
        ('skyBrightness', data.skyBrightness),
        ('cloud', data.cloud),
        ('seeing', data.seeing),
        ('slewTime', data.slewTime),
        ('cost', -1),
        ('rank', -1),
        ('propBoost', -1),
        ('numRequestingProps', data.numProposals),
        ('moonRA', data.moonRa),
        ('moonDec', data.moonDec),
        ('moonAlt', data.moonAlt),
        ('moonAz', data.moonAz),
        ('moonDistance', data.moonDistance),
        ('moonPhase', data.moonPhase),
        ('sunRA', data.sunRa),
        ('sunDec', data.sunDec),
        ('sunAlt', data.sunAlt),
        ('sunAz', data.sunAz),
        ('solarElong', data.solarElong)
    ])
    return values

def write_target_proposal_history(data, sid):
    """Create a dictionary of data for the TargetProposalHistory table.

    Parameters
    ----------
    data : tuple
        The instance containing the target proposal history information
    sid : int
        The current session ID.

    Returns
    -------
    collections.OrderedDict
        A dictionary of the topic data.
    """
    return ordered_dict_from_namedtuple(data, sid=sid)

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
