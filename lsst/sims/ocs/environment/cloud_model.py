import numpy
import os
import sqlite3

__all__ = ["CloudModel"]

class CloudModel(object):
    """Handle the cloud information.

    This class deals with the cloud information that was previously produced for
    OpSim version 3.
    """

    CLOUD_DB = "cloud.db"
    """Filename of the internal cloud observation database."""

    def __init__(self):
        """Initialize the class.
        """
        self.cloud_db = None
        self.cloud_dates = None
        self.cloud_values = None

    def get_cloud(self, delta_time):
        """Get the cloud for the specified time.

        Parameters
        ----------
        delta_time : int
            The time (seconds) from the start of the simulation.

        Returns
        -------
        float
            The cloud (arcseconds) closest to the specified time.
        """
        date = delta_time % self.cloud_dates[-1]
        date_delta = numpy.abs(self.cloud_dates - date)
        idx = numpy.where(date_delta == numpy.min(date_delta))
        return self.cloud_values[idx][0]

    def initialize(self, cloud_file=""):
        """Configure the cloud information.

        This function gets the appropriate database file and creates the cloud information
        from it. The default behavior is to use the module stored database. However, an
        alternate database file can be provided. The alternate database file needs to have a
        table called *Cloud* with the following columns:

        cloudId
            int : A unique index for each cloud entry.
        c_date
            int : The time (units=seconds) since the start of the simulation for the cloud observation.
        cloud
            float : The cloud coverage in 8ths of the sky.

        Parameters
        ----------
        cloud_file : str, optional
            The full path to an alternate cloud database.
        """
        if cloud_file != "":
            self.cloud_db = cloud_file
        else:
            self.cloud_db = os.path.join(os.path.dirname(__file__), self.CLOUD_DB)

        with sqlite3.connect(self.cloud_db) as conn:
            cur = conn.cursor()
            query = "select c_date, cloud from Cloud;"
            cur.execute(query)
            results = numpy.array(cur.fetchall())
            self.cloud_dates = numpy.hsplit(results, 2)[0].flatten()
            self.cloud_values = numpy.hsplit(results, 2)[1].flatten()
            cur.close()

    def write_to_db(self, db):
        """Write all the cloud information to the survey database.

        Parameters
        ----------
        db : :class:`.SocsDatabase`
            The instance of the survey database.
        """
        indicies = numpy.arange(1, self.cloud_dates.size + 1)
        cloud = list(map(tuple, numpy.hstack((indicies, self.cloud_dates,
                                              self.cloud_values)).reshape(-1, 3, order='F').tolist()))
        db.write_table("cloud", cloud)
