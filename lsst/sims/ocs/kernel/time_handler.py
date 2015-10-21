from datetime import datetime
from datetime import timedelta

SECONDS_IN_HOUR = 60.0 * 60.0
HOURS_IN_DAY = 24.0
SECONDS_IN_DAY = HOURS_IN_DAY * SECONDS_IN_HOUR
DAYS_IN_YEAR = 365.0
SECONDS_IN_YEAR = DAYS_IN_YEAR * SECONDS_IN_DAY

class TimeHandler(object):

    def __init__(self, initial_date):
        """Constructor for time handler class.

        This function is the constructor for the time handler class.

        Args:
            initial_date: A string in the format of YYYY-MM-DD containing the inital date.
        """
        self._unix_start = datetime(1970, 1, 1)
        self.initial_dt = datetime.strptime(initial_date, "%Y-%m-%d")
        self.current_dt = self.initial_dt

    def _time_difference(self, datetime1, datetime2=None):
        """Calculate the difference in seconds between two times.

        This function calculates the difference in seconds between to given datetime objects. If
        datetime2 is None, it is assumed to be _unix_start.

        Args:
            datetime1: The first datetime object.
            datetime2: The second datetime object.

        Returns:
            A float containing the difference in seconds between the two datetime objects.
        """
        if datetime2 is None:
            datetime2 = self._unix_start
        return (datetime1 - datetime2).total_seconds()

    @property
    def initial_timestamp(self):
        """Return the UNIX timestamp for the initial date/time.

        This function returns the UNIX timestamp for the initial_timestamp date/time.

        Returns:
            An float containing the UNIX timestamp for the initial date/time.
        """
        return self._time_difference(self.initial_dt)

    @property
    def current_timestamp(self):
        """Return the UNIX timestamp for the current date/time.

        This function returns the UNIX timestamp for the currently held date/time.

        Returns:
            An float containing the UNIX timestamp for the current date/time.
        """
        return self._time_difference(self.current_dt)

    def update_time(self, time_increment, time_units):
        """Update the currently held timestamp.

        This function updates the currently held time with the given increment and corresponding
        units.

        Args:
            time_increment: A float value containing the increment to adjust the current time.
            time_units: A string containing the time unit for the increment value.
        """
        time_delta_dict = {time_units: time_increment}
        self.current_dt += timedelta(**time_delta_dict)

    @property
    def current_timestring(self):
        """Return the ISO-8601 representation of the current date/time.

        This function returns the ISO-8601 formatted string of the currently held date/time.

        Returns:
            A string containing the ISO-8601 format for the current date/time.
        """
        return self.current_dt.isoformat()

    def has_time_elapsed(self, time_span):
        """Return a boolean determining if the time span has elapsed.

        This function looks to see if the time elapsed (current_time - initial_time) in units of
        seconds is greater or less than the requested time span. It will return true if the time span
        is greater than or equal the elapsed time and false if less than the elapsed time.

        Args:
            time_span: A float containing the requested time span in seconds.

        Return:
            A boolean determed if the time elapsed is greater or less than the time span.
        """
        return time_span >= self._time_difference(self.current_dt, self.initial_dt)

    def future_timestring(self, time_increment, time_units):
        """Give the ISO-8601 string for a future date/time.

           This function adds the requested time increment to the current date/time to get a future date/time
           and returns the ISO-8601 formatted string for that date/time.

           Args:
               time_increment: A float value containing the increment to adjust the current time.
               time_units: A string containing the time unit for the increment value.

           Returns:
               A string containing the ISO-8601 format for the future date/time.
        """
        time_delta_dict = {time_units: time_increment}
        return (self.current_dt + timedelta(**time_delta_dict)).isoformat()
