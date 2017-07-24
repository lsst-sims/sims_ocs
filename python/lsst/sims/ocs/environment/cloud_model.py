from builtins import object
from datetime import datetime
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

    def __init__(self, time_handler):
        """Initialize the class.

        Parameters
        ----------
        time_handler : :class:`.TimeHandler`
            The instance of the simulation time handler.
        """
        self.cloud_db = None
        self.cloud_dates = None
        self.cloud_values = None
        model_time_start = datetime(time_handler.initial_dt.year, 1, 1)
        self.offset = time_handler.time_since_given_datetime(model_time_start,
                                                             reverse=True)

    def get_cloud(self, delta_time):
        """Get the cloud for the specified time.

        Parameters
        ----------
        delta_time : int
            The time (seconds) from the start of the simulation.

        Returns
        -------
        float
            The cloud (fraction of sky in 8ths) closest to the specified time.
        """
        delta_time += self.offset
        date = delta_time % self.cloud_dates[-1]
        idx = numpy.searchsorted(self.cloud_dates, date)
        # searchsorted ensures that left < date < right
        # but we need to know if date is closer to left or to right
        left = self.cloud_dates[idx - 1]
        right = self.cloud_dates[idx]
        if date - left < right - date:
            idx -= 1
        return self.cloud_values[idx]

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
            query = "select c_date, cloud from Cloud order by c_date;"
            cur.execute(query)
            results = numpy.array(cur.fetchall())
            self.cloud_dates = numpy.hsplit(results, 2)[0].flatten()
            self.cloud_values = numpy.hsplit(results, 2)[1].flatten()
            cur.close()

    def set_topic(self, th, topic):
        """Set the cloud information into the topic.

        Parameters
        ----------
        th : :class:`TimeHandler`
            A time handling instance.
        topic : SALPY_scheduler.scheduler_cloudC
            An instance of the cloud topic.
        """
        topic.timestamp = th.current_timestamp
        topic.cloud = self.get_cloud(th.time_since_start)
