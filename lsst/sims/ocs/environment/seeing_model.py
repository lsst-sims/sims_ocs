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
    """Filename of the internal seeing observation database."""

    def __init__(self):
        """Initialize the class.
        """
        self.seeing_db = None
        self.seeing_dates = None
        self.seeing_values = None

    def get_seeing(self, delta_time):
        """Get the seeing for the specified time.

        Parameters
        ----------
        delta_time : int
            The time (seconds) from the start of the simulation.

        Returns
        -------
        float
            The seeing (arcseconds) closest to the specified time.
        """
        date = delta_time % self.seeing_dates[-1]
        date_delta = numpy.abs(self.seeing_dates - date)
        idx = numpy.where(date_delta == numpy.min(date_delta))
        return self.seeing_values[idx][0]

    def initialize(self, seeing_file=""):
        """Configure the seeing information.

        This function gets the appropriate database file and creates the seeing information
        from it. The default behavior is to use the module stored database. However, an
        alternate database file can be provided. The alternate database file needs to have a
        table called *Seeing* with the following columns:

        seeingId
            int : A unique index for each seeing entry.
        s_date
            int : The time (units=seconds) since the start of the simulation for the seeing observation.
        seeing
            float : The FWHM of the atmospheric PSF (units=arcseconds).

        Parameters
        ----------
        seeing_file : str, optional
            The full path to an alternate seeing database.
        """
        if seeing_file != "":
            self.seeing_db = seeing_file
        else:
            self.seeing_db = os.path.join(os.path.dirname(__file__), self.SEEING_DB)

        with sqlite3.connect(self.seeing_db) as conn:
            cur = conn.cursor()
            query = "select s_date, seeing from Seeing;"
            cur.execute(query)
            results = numpy.array(cur.fetchall())
            self.seeing_dates = numpy.hsplit(results, 2)[0].flatten()
            self.seeing_values = numpy.hsplit(results, 2)[1].flatten()
            cur.close()

    def write_to_db(self, db):
        """Write all the seeing information to the survey database.

        Parameters
        ----------
        db : :class:`.SocsDatabase`
            The instance of the survey database.
        """
        indicies = numpy.arange(1, self.seeing_dates.size + 1)
        seeing = list(map(tuple, numpy.hstack((indicies, self.seeing_dates,
                                               self.seeing_values)).reshape(-1, 3, order='F').tolist()))
        db.write_table("seeing", seeing)
