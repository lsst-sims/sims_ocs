from sqlalchemy import Column, Index, Integer, String, Table
from sqlalchemy.types import DATETIME
from sqlalchemy import DDL, event

def create_session(metadata, autoincrement=True):
    """Create Session table.

    This function creates the Session table for tracking the various simulations run. For MySQL, it adds
    a post-create command to set the lower limit of the auto increment value.

    Args:
        metadata (sqlalchemy.MetaData): The database object that collects the tables.
        autoincrement (bool): A flag to set auto incrementing on the sessionID column.

    Returns:
        (sqlalchemy.Table): The Session table object.
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
