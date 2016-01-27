from datetime import datetime
from datetime import timedelta

SECONDS_IN_HOUR = 60.0 * 60.0
HOURS_IN_DAY = 24.0
SECONDS_IN_DAY = HOURS_IN_DAY * SECONDS_IN_HOUR
DAYS_IN_YEAR = 365.0
SECONDS_IN_YEAR = DAYS_IN_YEAR * SECONDS_IN_DAY

__all__ = ["TimeHandler"]

class TimeHandler(object):
    """Keep track of simulation time information.

    Attributes
    ----------
    _unix_start : datetime.datetime
        Holder for the start of the UNIX epoch
    initial_dt : datetime.datetime
        The date/time of the simulation start.
    current_dt : datetime.datetime
        The current simulation date/time.
    """

    def __init__(self, initial_date):
        """Initialize the class.

        Parameters
        ----------
            initial_date : str
                The inital date in the format of YYYY-MM-DD.
        """
        self._unix_start = datetime(1970, 1, 1)
        self.initial_dt = datetime.strptime(initial_date, "%Y-%m-%d")
        self.current_dt = self.initial_dt

    def _time_difference(self, datetime1, datetime2=None):
        """Calculate the difference in seconds between two times.

        This function calculates the difference in seconds between two given :class:`datetime` instances. If
        datetime2 is None, it is assumed to be UNIX epoch start.

        Parameters
        ----------
        datetime1 : datetime.datetime
            The first datetime instance.
        datetime2 : datetime.datetime
            The second datetime instance.

        Returns
        -------
        float
            The difference in seconds between the two datetime instances.
        """
        if datetime2 is None:
            datetime2 = self._unix_start
        return (datetime1 - datetime2).total_seconds()

    @property
    def initial_timestamp(self):
        """float: Return the UNIX timestamp for the initial date/time.
        """
        return self._time_difference(self.initial_dt)

    @property
    def current_timestamp(self):
        """float: Return the UNIX timestamp for the current date/time.
        """
        return self._time_difference(self.current_dt)

    def update_time(self, time_increment, time_units):
        """Update the currently held timestamp.

        This function updates the currently held time with the given increment and corresponding
        units.

        Parameters
        ----------
        time_increment : float
            The increment to adjust the current time.
        time_units : str
            The time unit for the increment value.
        """
        time_delta_dict = {time_units: time_increment}
        self.current_dt += timedelta(**time_delta_dict)

    @property
    def current_timestring(self):
        """str: Return the ISO-8601 representation of the current date/time.
        """
        return self.current_dt.isoformat()

    def has_time_elapsed(self, time_span):
        """Return a boolean determining if the time span has elapsed.

        This function looks to see if the time elapsed (current_time - initial_time) in units of
        seconds is greater or less than the requested time span. It will return true if the time span
        is greater than or equal the elapsed time and false if less than the elapsed time.

        Parameters
        ----------
        time_span : float
            The requested time span in seconds.

        Returns
        -------
        bool
            True if the time elapsed is greater or False if less than the time span.
        """
        return time_span >= self._time_difference(self.current_dt, self.initial_dt)

    def future_timestring(self, time_increment, time_units):
        """Return the ISO-8601 representation of the future date/time.

        This function adds the requested time increment to the current date/time to get a future date/time
        and returns the ISO-8601 formatted string for that date/time. It does not update the internal
        timestamp.

        Parameters
        ----------
        time_increment : float
            The increment to adjust the current time.
        time_units : str
            The time unit for the increment value.

        Returns
        -------
        str
            The future date/time in ISO-8601.
        """
        time_delta_dict = {time_units: time_increment}
        return (self.current_dt + timedelta(**time_delta_dict)).isoformat()
