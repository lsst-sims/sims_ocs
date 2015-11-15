from sqlalchemy import Column, Index, Integer, String, Table
from sqlalchemy.types import DATETIME
from sqlalchemy import DDL, event

def create_session(metadata):
    table = Table("Session", metadata,
                  Column("sessionID", Integer, primary_key=True, autoincrement=True, nullable=False),
                  Column("sessionUser", String(80), nullable=False),
                  Column("sessionHost", String(80), nullable=False),
                  Column("sessionDate", DATETIME, nullable=False),
                  Column("version", String(25), nullable=True),
                  Column("runComment", String(200), nullable=True))

    Index("s_host_user_date_idx", table.c.sessionUser, table.c.sessionHost, table.c.sessionDate, unique=True)

    alter_table = DDL("ALTER TABLE '%(table)s' AUTO_INCREMENT=1000;")
    event.listen(table, 'after_create', alter_table.execute_if(dialect='mysql'))

    return table
