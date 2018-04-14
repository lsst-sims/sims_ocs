from lsst.sims.downtimeModel import UnscheduledDowntime

class UnscheduledDowntimeInterface(object):
    """Handle creating the unscheduled downtime information.

    This class handles the unscheduled downtime information.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.ud = UnscheduledDowntime()

    def __call__(self):
        """Return the top downtime.
        """
        return self.ud()

    def initialize(self, use_random_seed=False, random_seed=-1, survey_length=7300):
        """Configure the set of unscheduled downtimes.

        This function creates the unscheduled downtimes based on a set of probabilities
        of the downtime type occurance. A default seed is used to produce the same set of
        downtimes, but a randomized seed can be requested.

        The random downtime is calculated using the following probabilities:

        minor event
            remainder of night and next day = 5/365 days e.g. power supply failure
        intermediate
            3 nights = 2/365 days e.g. repair filter mechanism, rotator, hexapod, or shutter
        major event
            7 nights = 1/2*365 days
        catastrophic event
            14 nights = 1/3650 days e.g. replace a raft

        Parameters
        ----------
        use_random_seed : bool, optional
            Flag to set the seed based on the current time. Default is to used fixed seed.
        random_seed : int, optional
            Provide an alternate random seed. Only works when use_random_seed is True.
        survey_length : int, optional
            The length of the survey in days. Default is the length of a 20 year survey.
        """
        self.ud.initialize(use_random_seed=use_random_seed, random_seed=random_seed, survey_length=survey_length)

    def get_downtimes(self):
        return self.ud.downtimes

    def get_seed(self):
        return self.ud.seed