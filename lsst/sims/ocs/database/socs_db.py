import os

import MySQLdb as mysql
from sqlalchemy import create_engine, MetaData

from .tables.base_tbls import create_session
from ..utilities.session_info import get_hostname

class SocsDatabase(object):

    def __init__(self, dialect="mysql"):
        self.db_name = "SocsDB"
        self.db_dialect = dialect
        self.metadata = MetaData()
        self.engine = None
        self.db_save_dir = ""

        tbl = create_session(self.metadata)
        setattr(self, tbl.name.lower(), tbl)

    def _connect(self):
        conf_file = os.path.join(os.getenv("HOME"), ".my.cnf")
        return mysql.connect(read_default_file=conf_file, db=self.db_name)

    def _make_engine(self, initialize=True):
        if self.engine is None:
            if self.db_dialect == "mysql":
                self.engine = create_engine("mysql://", creator=self._connect)
            if self.db_dialect == "sqlite":
                if initialize:
                    session_tracking_db = "{}_sessions.db".format(get_hostname())
                    self.engine = create_engine("sqlite:///{}".format(session_tracking_db))

    def create_db(self):
        self._make_engine()
        self.metadata.create_all(self.engine)

    def delete_db(self):
        self._make_engine()
        self.metadata.drop_all(self.engine)
