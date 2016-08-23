import numpy
import os
import sqlite3

__all__ = ["SeeingModel"]

class SeeingModel(object):
    """Handle the seeing information.

    This class deals with the seeing information that was previously produced for
    OpSim version 3.
    """

    SEEING_DB = "seeing.db"

    def __init__(self):
        """Initialize the class.
        """
        self.seeing_db = None
        self.seeing_dates = None
        self.seeing_values = None

    def initialize(self):
        """Configure the seeing information.
        """

        self.seeing_db = os.path.join(os.path.dirname(__file__), self.SEEING_DB)

        with sqlite3.connect(self.seeing_db) as conn:
            cur = conn.cursor()
            query = "select s_date, seeing from Seeing;"
            cur.execute(query)
            results = numpy.array(cur.fetchall())
            self.seeing_dates = numpy.hsplit(results, 2)[0].flatten()
            self.seeing_values = numpy.hsplit(results, 2)[1].flatten()
            cur.close()
