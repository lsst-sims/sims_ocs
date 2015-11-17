from datetime import datetime
import os

import MySQLdb as mysql
from sqlalchemy import create_engine, MetaData

from .tables.base_tbls import create_session
from ..utilities.session_info import get_hostname, get_user, get_version

class SocsDatabase(object):
    """Main class for simulation database interaction.

    This class is responsible for interacting with the main simulation database. For MySQL, this is a central
    database containing all the relevant tables. For SQLite, this consists of a machine session tracking
    database and individual database files for each run session of the simulation.
    """

    SQLITE_SESSION_OFFSET = 999

    def __init__(self, dialect="mysql", mysql_config_path=None, sqlite_save_path=None):
        """Class constructor.

        Args:
            dialect (str): The flavor of the database to use. Options: mysql or sqlite.
            mysql_config_path (str): An alternate path for the .my.cnf configuration file for MySQL.
            sqlite_save_path (str): A path to save all resulting database files for SQLite.
        """
        self.db_name = "SocsDB"
        self.db_dialect = dialect
        self.metadata = MetaData()
        self.engine = None
        self.mysql_config_path = mysql_config_path
        self.sqlite_save_path = sqlite_save_path

        # Parameters for SQLite operations
        self.session_engine = None
        self.session_metadata = MetaData()

        if self.db_dialect == "mysql":
            self._create_tables()
            self.engine = self._make_engine()
        if self.db_dialect == "sqlite":
            self.session_tracking = create_session(self.metadata)
            sqlite_session_tracking_db = "{}_sessions.db".format(get_hostname())
            self.engine = self._make_engine(sqlite_session_tracking_db)

    def _create_tables(self, metadata=None, use_autoincrement=True):
        """Create all the relevant tables.

        Args:
            use_autoincrement (bool): A flag to set auto increment behavior on the Session table.
        """
        if metadata is None:
            metadata = self.metadata
        self.session = create_session(metadata, use_autoincrement)

    def _connect(self):
        """Create the database connection for MySQL.1

        Returns:
            (function): The connection function for MySQL.
        """
        if self.mysql_config_path is not None:
            conf_path = self.mysql_config_path
        else:
            conf_path = os.getenv("HOME")
        conf_file = os.path.join(conf_path, ".my.cnf")
        return mysql.connect(read_default_file=conf_file, db=self.db_name)

    def _make_engine(self, sqlite_db=None):
        """Create the engine for database interactions.

        Args:
            sqlite_db (str): The name of the database file for SQLite.
        """
        if self.db_dialect == "mysql":
            return create_engine("mysql://", creator=self._connect)
        if self.db_dialect == "sqlite":
            if self.sqlite_save_path is not None:
                sqlite_db = os.path.join(self.sqlite_save_path, sqlite_db)
            return create_engine("sqlite:///{}".format(sqlite_db))

    def create_db(self):
        """Create the database tables.

        This function does the actual work of creating all the relevant database tables. For MySQL, these
        go into the central database. For SQLite, this creates the session tracking database with the Session
        table.
        """
        self.metadata.create_all(self.engine)

    def delete_db(self):
        """Delete all database tables.

        This function only works for MySQL. It will have no effect on SQLite.
        """
        self.metadata.drop_all(self.engine)

    def new_session(self, run_comment):
        """Log a new session to the database and return the ID.

        This function logs a new session to the database and returns the session ID. For MySQL, this writes
        to the Session table in the central database. For SQLite, this writes an entry to the session tracking
        database. Then a session ID specific database is created and the information is replicated in that
        Session table. Since SQLite auto increment values always start at one, an offset is applied to make
        the session IDs commensurate with MySQL.

        Args:
            run_comment (str): The startup comment for the simulation run.

        Returns:
            int: The session ID for this simulation run.
        """
        hostname = get_hostname()
        user = get_user()
        version = get_version()
        date = datetime.utcnow()
        if self.db_dialect == "mysql":
            date = date.strftime("%Y-%m-%d %H:%M:%S")

        if self.db_dialect == "mysql":
            s = self.session
        if self.db_dialect == "sqlite":
            s = self.session_tracking
        insert = s.insert()
        conn = self.engine.connect()
        result = conn.execute(insert, sessionUser=user, sessionHost=hostname, sessionDate=date,
                              version=version, runComment=run_comment)

        session_id = result.lastrowid

        if self.db_dialect == "sqlite":
            session_id += self.SQLITE_SESSION_OFFSET
            sqlite_session_db = "{}_{}.db".format(get_hostname(), session_id)
            self.session_engine = self._make_engine(sqlite_session_db)
            self._create_tables(self.session_metadata, use_autoincrement=False)
            self.session_metadata.create_all(self.session_engine)
            insert = self.session.insert()
            conn = self.session_engine.connect()
            result = conn.execute(insert, session_ID=session_id, sessionUser=user, sessionHost=hostname,
                                  sessionDate=date, version=version, runComment=run_comment)

        return session_id
