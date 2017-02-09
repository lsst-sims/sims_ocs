import logging
import random
import time

from lsst.sims.ocs.setup import LoggingLevel

class UnscheduledDowntime(object):
    """Handle creating the unscheduled downtime information.

    This class handles the unscheduled downtime information.
    """

    MINOR_EVENT = (0.0137, 1, "minor event")
    INTERMEDIATE_EVENT = (0.00548, 3, "intermediate event")
    MAJOR_EVENT = (0.00137, 7, "major event")
    CATASTROPHIC_EVENT = (0.000274, 14, "catastrophic event")

    def __init__(self):
        """Initialize the class.
        """
        self.seed = 1516231120
        self.downtimes = []
        self.log = logging.getLogger("downtime.UnscheduledDowntime")

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

    @property
    def total_downtime(self):
        """Get the total downtime (units=days).

        Returns
        -------
        int
        """
        return sum([x[1] for x in self.downtimes])

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
        if use_random_seed:
            if random_seed == -1:
                self.seed = int(time.time())
            else:
                self.seed = random_seed

        random.seed(self.seed)

        nights = 0
        while nights < survey_length:
            prob = random.random()
            if prob < self.CATASTROPHIC_EVENT[0]:
                self.downtimes.append((nights, self.CATASTROPHIC_EVENT[1], self.CATASTROPHIC_EVENT[2]))
                nights += self.CATASTROPHIC_EVENT[1] + 1
                continue
            else:
                prob = random.random()
                if prob < self.MAJOR_EVENT[0]:
                    self.downtimes.append((nights, self.MAJOR_EVENT[1], self.MAJOR_EVENT[2]))
                    nights += self.MAJOR_EVENT[1] + 1
                    continue
                else:
                    prob = random.random()
                    if prob < self.INTERMEDIATE_EVENT[0]:
                        self.downtimes.append((nights, self.INTERMEDIATE_EVENT[1],
                                               self.INTERMEDIATE_EVENT[2]))
                        nights += self.INTERMEDIATE_EVENT[1] + 1
                        continue
                    else:
                        prob = random.random()
                        if prob < self.MINOR_EVENT[0]:
                            self.downtimes.append((nights, self.MINOR_EVENT[1], self.MINOR_EVENT[2]))
            nights += 1

        self.log.log(LoggingLevel.WORDY.value,
                     "Total unscheduled downtime: {} days in {} days.".format(self.total_downtime,
                                                                              survey_length))
