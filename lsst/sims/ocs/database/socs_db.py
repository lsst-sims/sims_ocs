import os

import MySQLdb as mysql
from sqlalchemy import create_engine, MetaData

from .tables.base_tbls import create_session
from ..utilities.session_info import get_hostname

class SocsDatabase(object):
    """Main class for simulation database interaction.

    This class is responsible for interacting with the main simulation database. For MySQL, this is a central
    database containing all the relevant tables. For SQLite, this consists of a machine session tracking
    database and individual database files for each run session of the simulation.
    """

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

        if self.db_dialect == "mysql":
            self._create_tables()
        if self.db_dialect == "sqlite":
            self.session_tracking = create_session(self.metadata)

    def _create_tables(self, use_autoincrement=True):
        """Create all the relevant tables.

        Args:
            use_autoincrement (bool): A flag to set auto increment behavior on the Session table.
        """
        self.session = create_session(self.metadata, use_autoincrement)

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
        if self.engine is None:
            if self.db_dialect == "mysql":
                self.engine = create_engine("mysql://", creator=self._connect)
            if self.db_dialect == "sqlite":
                self.engine = create_engine("sqlite:///{}".format(sqlite_db))

    def create_db(self):
        """Create the database tables.

        This function does the actual work of creating all the relevant database tables. For MySQL, these
        go into the central database. For SQLite, this creates the session tracking database with the Session
        table.
        """
        if self.db_dialect == "sqlite":
            sqlite_session_tracking_db = "{}_sessions.db".format(get_hostname())
            if self.sqlite_save_path is not None:
                sqlite_session_tracking_db = os.path.join(self.sqlite_save_path, sqlite_session_tracking_db)
            self._make_engine(sqlite_session_tracking_db)
        else:
            self._make_engine()
        self.metadata.create_all(self.engine)

    def delete_db(self):
        """Delete all database tables.

        This function only works for MySQL. It will have no effect on SQLite.
        """
        self._make_engine()
        self.metadata.drop_all(self.engine)
