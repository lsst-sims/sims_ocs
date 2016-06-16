import pkg_resources
import sqlite3

class ScheduledDowntime(object):
    """Handle the scheduled downtime information.

    This class handles the scheduled downtime information.
    """

    SCHEDULED_DOWNTIME_DB = "scheduled_downtime.db"

    def __init__(self):
        """Initialize the class.
        """
        self.downtime_file = None
        self.downtimes = []

    def __call__(self):
        """Return the top downtime.
        """
        try:
            return self.downtimes.pop(0)
        except IndexError:
            return None

    def __len__(self):
        """Return number of scheduled downtimes.

        Returns
        -------
        int
        """
        return len(self.downtimes)

    def initialize(self, downtime_file=None):
        """Configure the set of scheduled downtimes.

        This function gets the appropriate database file and creates the set of
        scheduled downtimes from it. The default behavior is to use the module stored
        database. However, an alternate database file can be provided. The alternate
        database file needs to have a table called *Downtime* with the following columns:

        night
            int : The night (from start of simulation) the downtime occurs.
        duration
            int : The duration (units=days) of the downtime.
        activity
            str : A description of the activity involved.

        Parameters
        ----------
        downtime_file : str
            A full path to an alternate scheduled downtime database file.
        """

        if downtime_file is not None:
            self.downtime_file = downtime_file
        else:
            rsman = pkg_resources.ResourceManager()
            self.downtime_file = rsman.resource_filename("lsst.sims.ocs",
                                                         "downtime/{}".format(self.SCHEDULED_DOWNTIME_DB))

        with sqlite3.connect(self.downtime_file) as conn:
            cur = conn.cursor()
            cur.execute("select * from Downtime;")
            for row in cur:
                self.downtimes.append((row[0], row[1], row[2]))
            cur.close()
