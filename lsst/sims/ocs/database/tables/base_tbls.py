from sqlalchemy import Column, Float, Index, Integer, String, Table
from sqlalchemy.types import DATETIME
from sqlalchemy import DDL, event

__all__ = ["create_field", "create_observation_history", "create_session",
           "create_slew_history", "create_target_history"]

def create_session(metadata, autoincrement=True):
    """Create Session table.

    This function creates the Session table for tracking the various simulations run. For MySQL, it adds
    a post-create command to set the lower limit of the auto increment value.

    Parameters
    ----------
    metadata : sqlalchemy.MetaData
        The database object that collects the tables.
    autoincrement : bool
        A flag to set auto incrementing on the sessionID column.

    Returns
    -------
    sqlalchemy.Table
        The Session table object.
    """
    table = Table("Session", metadata,
                  Column("sessionID", Integer, primary_key=True, autoincrement=autoincrement, nullable=False),
                  Column("sessionUser", String(80), nullable=False),
                  Column("sessionHost", String(80), nullable=False),
                  Column("sessionDate", DATETIME, nullable=False),
                  Column("version", String(25), nullable=True),
                  Column("runComment", String(200), nullable=True))

    Index("s_host_user_date_idx", table.c.sessionUser, table.c.sessionHost, table.c.sessionDate, unique=True)

    alter_table = DDL("ALTER TABLE %(table)s AUTO_INCREMENT=1000;")
    event.listen(table, 'after_create', alter_table.execute_if(dialect='mysql'))

    return table

def create_field(metadata):
    """Create Field table.

    This function creates the Field table from the sky tesellation.

    Parameters
    ----------
    metadata : sqlalchemy.MetaData
        The database object that collects the tables.

    Returns
    -------
    sqlalchemy.Table
        The Field table object.
    """
    table = Table("Field", metadata,
                  Column("ID", Integer, primary_key=True, nullable=False),
                  Column("fov", Float, nullable=False),
                  Column("ra", Float, nullable=False),
                  Column("dec", Float, nullable=False),
                  Column("gl", Float, nullable=False),
                  Column("gb", Float, nullable=False),
                  Column("el", Float, nullable=False),
                  Column("eb", Float, nullable=False))

    Index("field_fov", table.c.ID, table.c.fov)
    Index("fov_gl_gb", table.c.fov, table.c.gl, table.c.gb)
    Index("fov_el_eb", table.c.fov, table.c.el, table.c.eb)
    Index("fov_ra_dec", table.c.fov, table.c.ra, table.c.dec)

    return table

def create_target_history(metadata):
    """Create TargetHistory table.

    This function creates the TargetHistory table for tracking all the requested targets from
    the Scheduler in the simulation run.

    Parameters
    ----------
    metadata : sqlalchemy.MetaData
        The database object that collects the tables.

    Returns
    -------
    sqlalchemy.Table
        The TargetHistory table object.
    """
    table = Table("TargetHistory", metadata,
                  Column("targetID", Integer, primary_key=True),
                  Column("Session_sessionID", Integer, primary_key=True),
                  Column("fieldID", Integer),
                  Column("filter", String(1)),
                  Column("ra", Float),
                  Column("dec", Float),
                  Column("angle", Float),
                  Column("num_exposures", Integer))

    Index("t_filter", table.c.filter)
    Index("fk_TargetHistory_Session1", table.c.Session_sessionID)
    Index("fk_TargetHistory_Field1", table.c.fieldID)

    return table

def create_observation_history(metadata):
    """Create ObsHistory table.

    This function creates the ObsHistory table for tracking all the observations performed
    by the Sequencer in the simulation run.

    Parameters
    ----------
    metadata : sqlalchemy.MetaData
        The database object that collects the tables.

    Returns
    -------
    sqlalchemy.Table
        The ObsHistory table object.
    """
    table = Table("ObsHistory", metadata,
                  Column("observationID", Integer, primary_key=True),
                  Column("Session_sessionID", Integer, primary_key=True),
                  Column('observationTime', Float),
                  Column('targetID', Integer),
                  Column("fieldID", Integer),
                  Column("filter", String(1)),
                  Column("ra", Float),
                  Column("dec", Float),
                  Column("angle", Float),
                  Column("num_exposures", Integer))

    Index("o_filter", table.c.filter)
    Index("fk_ObsHistory_Session1", table.c.Session_sessionID)
    Index("fk_ObsHistory_Field1", table.c.fieldID)
    Index("fk_ObsHistory_Target1", table.c.targetID)

    return table

def create_slew_history(metadata):
    """Create SlewHistory table.

    This function creates the SlewHistory table for tracking all the general slew information
    performed by the observatory.

    Parameters
    ----------
    metadata : sqlalchemy.MetaData
        The database object that collects the tables.

    Returns
    -------
    sqlalchemy.Table
        The SlewHistory table object.
    """
    table = Table("SlewHistory", metadata,
                  Column("slewCount", Integer, primary_key=True, nullable=False),
                  Column("startDate", Float, nullable=False),
                  Column("endDate", Float, nullable=False),
                  Column("slewTime", Float, nullable=False),
                  Column("slewDistance", Float, nullable=False),
                  Column("ObsHistory_observationID", Integer))

    Index("fk_SlewHistory_ObsHistory1", table.c.ObsHistory_observationID)

    return table
