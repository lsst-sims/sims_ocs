import collections

def write_target_history(data, sid):
    """Create a dictionary of data for the TargetHistory table.

    Args:
        data (SALPY_scheduler.targetTestC): The SAL target topic instance.
        sid (int): The current session ID.

    Returns:
        collections.OrderedDict: A dictionary of the topic data.
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

def write_field(data):
    """Create a dictionary of data for the Field table.

    Args:
        data (SALPY_scheduler.fieldC): The SAL target topic instance.

    Returns:
        collections.OrderedDict: A dictionary of the topic data.
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
