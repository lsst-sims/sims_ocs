from __future__ import absolute_import
from builtins import object
import collections
from datetime import datetime
import logging
import numpy
import os
from sqlalchemy import create_engine, desc, exc, MetaData

from lsst.sims.ocs.setup import LoggingLevel
from . import tables
from lsst.sims.ocs.utilities import expand_path, get_hostname, get_user, get_version
from lsst.sims.ocs.utilities.socs_exceptions import SocsDatabaseError

__all__ = ["SocsDatabase"]

class SocsDatabase(object):
    """Main class for simulation database interaction.

    This class is responsible for interacting with the main SQLite simulation database.
    This consists of a machine session tracking database and individual database files
    for each run session of the simulation.

    Attributes
    ----------
    db_dialect : str
        The flavor of the database to use. Options: sqlite.
    metadata : sqlalchemy.MetaData
        The instance for holding the relevant tables.
    engine : sqlalchemy.engine.Engine
        The instance of the database engine.
    sqlite_save_path : str
        A path to save all resulting database files for SQLite.
    sqlite_session_save_path : str
        A path to save the SQLite session tracking database.
    session_engine : sqlalchemy.engine.Engine
        The session specific instance of the database engine. SQLite only.
    session_metadata : sqlalchemy.MetaData
        The instance for holding the session specific tables. SQLite only.
    session_start : int
        A new starting session Id for counting new simulations.
    """

    def __init__(self, sqlite_save_path=None, session_id_start=None, sqlite_session_save_path=None):
        """Initialize the class.

        Parameters
        ----------
        sqlite_save_path : str
            A path to save all resulting database files for SQLite.
        session_id_start : int
            A new starting session Id for counting new simulations.
        """
        self.log = logging.getLogger("database.SocsDatabase")
        self.db_dialect = "sqlite"
        self.session_id = -1
        self.session_start = session_id_start if session_id_start is not None else 2000
        self.metadata = MetaData()
        self.engine = None
        self.sqlite_save_path = sqlite_save_path
        self.sqlite_session_save_path = sqlite_session_save_path

        # Parameters for SQLite operations
        self.session_engine = None
        self.session_metadata = MetaData()

        self.session_tracking = tables.create_session(self.metadata, autoincrement=False)
        sqlite_session_tracking_db = "{}_sessions.db".format(get_hostname())
        self.engine = self._make_engine(sqlite_session_tracking_db, self.sqlite_session_save_path)

        # Parameter for holding data lists
        self.data_list = collections.defaultdict(list)

    @property
    def data_empty(self):
        """bool: Is internal data list empty
        """
        return len(self.data_list) == 0

    def _create_tables(self, metadata=None, use_autoincrement=True, session_id_start=2000):
        """Create all the relevant tables.

        Parameters
        ----------
        metadata : sqlalchemy.MetaData
            The instance for holding the relevant tables.
        use_autoincrement: bool
            A flag to set auto increment behavior on the Session table.
        session_id_start : int
            A new starting session Id for counting new simulations.
        """
        if metadata is None:
            metadata = self.metadata
        self.session = tables.create_session(metadata, use_autoincrement, session_id_start)
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
        self.proposal_field = tables.create_proposal_field(metadata)
        self.observation_proposal_history = tables.create_observation_proposal_history(metadata)
        self.target_proposal_history = tables.create_target_proposal_history(metadata)
        self.config = tables.create_config(metadata)
        self.summary_all_props = tables.create_summary_all_props(metadata, self.observation_history,
                                                                 self.slew_history, self.slew_initial_state,
                                                                 self.proposal,
                                                                 self.observation_proposal_history,
                                                                 self.field)

    def _make_engine(self, sqlite_db=None, alternate_save_path=None):
        """Create the engine for database interactions.

        Parameters
        ----------
        sqlite_db : str
            The name of the database file for SQLite.
        alternate_save_path : str, optional
            Specify an alternate path to save the database.
        """
        save_path = None
        if self.sqlite_save_path is not None:
            save_path = expand_path(self.sqlite_save_path)
        if alternate_save_path is not None:
            save_path = expand_path(alternate_save_path)
        if save_path is not None:
            sqlite_db = os.path.join(save_path, sqlite_db)
        return create_engine("sqlite:///{}".format(sqlite_db))

    def create_db(self):
        """Create the database tables.

        This function does the actual work of creating all the relevant database tables.
        This creates the session tracking database with the Session table.
        """
        self.metadata.create_all(self.engine)

    def new_session(self, run_comment):
        """Log a new session to the database and return the ID.

        This function logs a new session to the database and returns the session ID.
        This writes an entry to the session tracking database. Then a session ID
        specific database is created and the information is replicated in that
        Session table. Since SQLite auto increment values always start at one, an
        offset is applied to make the session IDs commensurate with OpSim3 style ones.

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

        # Get the session ID from the tracking file unless it was just created.
        conn = self.engine.connect()
        select = self.session_tracking.select().order_by(desc(self.session_tracking.c.sessionId)).limit(1)
        result = conn.execute(select)
        row = result.fetchone()
        try:
            self.session_id = int(row[0]) + 1
        except TypeError:
            self.session_id = self.session_start

        insert = self.session_tracking.insert()
        result = conn.execute(insert, sessionId=self.session_id, sessionUser=user, sessionHost=hostname,
                              sessionDate=date, version=version, runComment=run_comment)

        # Create the database for the given session ID.
        sqlite_session_db = "{}_{}.db".format(get_hostname(), self.session_id)
        self.session_engine = self._make_engine(sqlite_session_db)
        self._create_tables(self.session_metadata, use_autoincrement=False)
        self.session_metadata.create_all(self.session_engine)
        insert = self.session.insert()
        conn = self.session_engine.connect()
        result = conn.execute(insert, sessionId=self.session_id, sessionUser=user, sessionHost=hostname,
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
        e = self.session_engine
        return e.connect()

    def write(self):
        """Write collected information into the database.
        """
        conn = self._get_conn()

        db_errors = []
        for table_name, table_data in self.data_list.items():
            try:
                self.log.log(LoggingLevel.EXTENSIVE.value, "Writing {} data into DB.".format(table_name))
                self.log.log(LoggingLevel.EXTENSIVE.value, "Length of data: {}".format(len(table_data)))
                tbl = getattr(self, table_name)
                conn.execute(tbl.insert(), table_data)
            except exc.IntegrityError as err:
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
                db_errors.append(err.message)
        if len(db_errors):
            raise SocsDatabaseError(os.linesep.join(db_errors))

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
