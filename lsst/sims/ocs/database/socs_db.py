import os

import MySQLdb as mysql
from sqlalchemy import create_engine, MetaData

from .tables.base_tbls import create_session

class SocsDatabase(object):

    def __init__(self):
        self.db_name = "SocsDB"
        self.metadata = MetaData()
        self.engine = None

        tbl = create_session(self.metadata)
        setattr(self, tbl.name.lower(), tbl)

    def _connect(self):
        conf_file = os.path.join(os.getenv("HOME"), ".my.cnf")
        return mysql.connect(read_default_file=conf_file, database=self.db_name)

    def _make_engine(self):
        if self.engine is None:
            self.engine = create_engine("mysql://", creator=self._connect)

    def create_db(self):
        self._make_engine()
        self.metadata.create_all(self.engine)

    def delete_db(self):
        self._make_engine()
        self.metadata.drop_all(self.engine)
