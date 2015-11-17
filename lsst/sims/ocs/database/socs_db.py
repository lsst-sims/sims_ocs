import os

import MySQLdb as mysql
from sqlalchemy import create_engine, MetaData

from .tables.base_tbls import create_session
from ..utilities.session_info import get_hostname

class SocsDatabase(object):

    def __init__(self, dialect="mysql", mysql_config_path=None, sqlite_save_path=None):
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
        self.session = create_session(self.metadata, use_autoincrement)

    def _connect(self):
        if self.mysql_config_path is not None:
            conf_path = self.mysql_config_path
        else:
            conf_path = os.getenv("HOME")
        conf_file = os.path.join(conf_path, ".my.cnf")
        return mysql.connect(read_default_file=conf_file, db=self.db_name)

    def _make_engine(self, sqlite_db=None):
        if self.engine is None:
            if self.db_dialect == "mysql":
                self.engine = create_engine("mysql://", creator=self._connect)
            if self.db_dialect == "sqlite":
                self.engine = create_engine("sqlite:///{}".format(sqlite_db))

    def create_db(self):
        if self.db_dialect == "sqlite":
            sqlite_session_tracking_db = "{}_sessions.db".format(get_hostname())
            if self.sqlite_save_path is not None:
                sqlite_session_tracking_db = os.path.join(self.sqlite_save_path, sqlite_session_tracking_db)
            self._make_engine(sqlite_session_tracking_db)
        else:
            self._make_engine()
        self.metadata.create_all(self.engine)

    def delete_db(self):
        self._make_engine()
        self.metadata.drop_all(self.engine)
