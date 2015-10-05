class Simulator(object):

    def __init__(self, sim_duration):
        """Constructor for the Simulator class.

        This function is the constructor for the Simluator class.

        Args:
            sim_duration: A float value for the simulation duraction in fractions of a year.
        """
        self.fractional_duration = sim_duration

    @property
    def duration(self):
        """The duration of the simulation in days.

        This property reports the number of days in the simulation.
        """
        return round(self.fractional_duration * 365.0)

    def initialize(self):
        pass

    def run(self):
        pass

    def finalize(self):
        pass
