from lsst.sims.downtimeModel import ScheduledDowntime

class ScheduledDowntimeInterface(object):
    """Handle the scheduled downtime information.

    This class handles the scheduled downtime information.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.dt = ScheduledDowntime()

    def __call__(self):
        """Return the top downtime.
        """
        return self.dt()
 
    def initialize(self, downtime_file=""):
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
        downtime_file : str, optional
            A full path to an alternate scheduled downtime database file.
        """
        self.dt.initialize(downtime_file)

    def get_downtimes(self):

        return self.dt.downtimes