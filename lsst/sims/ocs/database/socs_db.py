import collections
from datetime import datetime
import logging
import MySQLdb as mysql
import numpy
import os
from sqlalchemy import create_engine, MetaData, exc

from lsst.sims.ocs.setup import LoggingLevel
import tables
from lsst.sims.ocs.utilities import expand_path, get_hostname, get_user, get_version

__all__ = ["SocsDatabase"]

class SocsDatabase(object):
    """Main class for simulation database interaction.

    This class is responsible for interacting with the main simulation database. For MySQL, this is a central
    database containing all the relevant tables. For SQLite, this consists of a machine session tracking
    database and individual database files for each run session of the simulation.

    Attributes
    ----------
    db_name : str
        The name of the database. Applies to MySQL only.
    db_dialect : str
        The flavor of the database to use. Options: mysql or sqlite.
    metadata : sqlalchemy.MetaData
        The instance for holding the relevant tables.
    engine : sqlalchemy.engine.Engine
        The instance of the database engine.
    mysql_config_path : str
        An alternate path for the .my.cnf configuration file for MySQL.
    sqlite_save_path : str
        A path to save all resulting database files for SQLite.
    session_engine : sqlalchemy.engine.Engine
        The session specific instance of the database engine. SQLite only.
    session_metadata : sqlalchemy.MetaData
        The instance for holding the session specific tables. SQLite only.
    """

    SQLITE_SESSION_OFFSET = 999
    """int: Adjustment so starting session ID is 1000 like MySQL."""

    def __init__(self, dialect="mysql", mysql_config_path=None, sqlite_save_path=None):
        """Initialize the class.

        Parameters
        ----------
        dialect : str
            The flavor of the database to use. Options: mysql or sqlite.
        mysql_config_path : str
            An alternate path for the .my.cnf configuration file for MySQL.
        sqlite_save_path : str
            A path to save all resulting database files for SQLite.
        """
        self.db_name = "SocsDB"
        self.log = logging.getLogger("database.SocsDatabase")
        self.db_dialect = dialect
        self.session_id = -1
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
            self.session_tracking = tables.create_session(self.metadata)
            sqlite_session_tracking_db = "{}_sessions.db".format(get_hostname())
            self.engine = self._make_engine(sqlite_session_tracking_db)

        # Parameter for holding data lists
        self.data_list = collections.defaultdict(list)

    def _create_tables(self, metadata=None, use_autoincrement=True):
        """Create all the relevant tables.

        Parameters
        ----------
        use_autoincrement: bool
            A flag to set auto increment behavior on the Session table.
        """
        if metadata is None:
            metadata = self.metadata
        self.session = tables.create_session(metadata, use_autoincrement)
        self.field = tables.create_field(metadata)
        self.target_history = tables.create_target_history(metadata)
        self.observation_history = tables.create_observation_history(metadata)
        self.slew_history = tables.create_slew_history(metadata)
        self.slew_initial_state = tables.create_slew_initial_state(metadata)
        self.slew_final_state = tables.create_slew_final_state(metadata)
        self.slew_activities = tables.create_slew_activities(metadata)
        self.slew_maxspeeds = tables.create_slew_maxspeeds(metadata)
        self.target_exposures = tables.create_target_exposures(metadata)
        self.observation_exposures = tables.create_observation_exposures(metadata)
        self.scheduled_downtime = tables.create_scheduled_downtime(metadata)
        self.unscheduled_downtime = tables.create_unscheduled_downtime(metadata)
        self.proposal = tables.create_proposal(metadata)
        self.proposal_history = tables.create_proposal_history(metadata)
        # self.seeing = tables.create_seeing(metadata)
        # self.cloud = tables.create_cloud(metadata)

    def _connect(self):
        """Create the database connection for MySQL.

        Returns
        -------
        function
            The connection function for MySQL.
        """
        if self.mysql_config_path is not None:
            conf_path = expand_path(self.mysql_config_path)
        else:
            conf_path = os.getenv("HOME")
        conf_file = os.path.join(conf_path, ".my.cnf")
        return mysql.connect(read_default_file=conf_file, db=self.db_name)

    def _make_engine(self, sqlite_db=None):
        """Create the engine for database interactions.

        Parameters
        ----------
        sqlite_db : str
            The name of the database file for SQLite.
        """
        if self.db_dialect == "mysql":
            return create_engine("mysql://", creator=self._connect)
        if self.db_dialect == "sqlite":
            if self.sqlite_save_path is not None:
                self.sqlite_save_path = expand_path(self.sqlite_save_path)
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

        Note
        ----
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

        Parameters
        ----------
        run_comment: str
            The startup comment for the simulation run.

        Returns
        -------
        int
            The session ID for this simulation run.
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

        self.session_id = result.lastrowid

        if self.db_dialect == "sqlite":
            self.session_id += self.SQLITE_SESSION_OFFSET
            sqlite_session_db = "{}_{}.db".format(get_hostname(), self.session_id)
            self.session_engine = self._make_engine(sqlite_session_db)
            self._create_tables(self.session_metadata, use_autoincrement=False)
            self.session_metadata.create_all(self.session_engine)
            insert = self.session.insert()
            conn = self.session_engine.connect()
            result = conn.execute(insert, session_ID=self.session_id, sessionUser=user, sessionHost=hostname,
                                  sessionDate=date, version=version, runComment=run_comment)

        return self.session_id

    def append_data(self, table_name, table_data):
        """Collect information for the provided table.

        Parameters
        ----------
        table_name: str
            The attribute name holding the sqlalchemy.Table instance.
        table_data: topic
            The Scheduler topic data instance.
        """
        write_func = getattr(tables, "write_{}".format(table_name))
        result = write_func(table_data, self.session_id)
        self.data_list[table_name].append(result)

    def clear_data(self):
        """Clear all stored data lists.
        """
        self.data_list.clear()
        self.log.log(LoggingLevel.EXTENSIVE.value, "After clearing: {}".format(self.data_list))

    def _get_conn(self):
        """Get the DB connection.

        Returns
        -------
        sqlalchemy.engine.Connection
            The DB connection for the associated type.
        """
        if self.db_dialect == "mysql":
            e = self.engine
        if self.db_dialect == "sqlite":
            e = self.session_engine
        return e.connect()

    def write(self):
        """Write collected information into the database.
        """
        conn = self._get_conn()

        for table_name, table_data in self.data_list.items():
            try:
                self.log.log(LoggingLevel.EXTENSIVE.value, "Writing {} data into DB.".format(table_name))
                self.log.log(LoggingLevel.EXTENSIVE.value, "Length of data: {}".format(len(table_data)))
                tbl = getattr(self, table_name)
                conn.execute(tbl.insert(), table_data)
            except exc.IntegrityError:
                self.log.error("Database insertion failed for {}!".format(table_name))
                output = collections.defaultdict(list)
                for values in table_data:
                    for k, v in values.items():
                        output[k].append(v)

                for k, v in output.items():
                    output[k] = numpy.array(v)

                filename = "{}_{}.npz".format(table_name, self.session_id)
                numpy.savez(open(filename, 'w'), **output)
                self.log.error("Dumping information into {}".format(filename))
                raise

    def write_table(self, table_name, table_data):
        """Collect information for the provided table.

        Parameters
        ----------
        table_name : str
            The attribute name holding the sqlalchemy.Table instance.
        table_data : list[topic]
            A set of Scheduler topic data instances.
        """
        conn = self._get_conn()
        tbl = getattr(self, table_name)
        conn.execute(tbl.insert(), table_data)
