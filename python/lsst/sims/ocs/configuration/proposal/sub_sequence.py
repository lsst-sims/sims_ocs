import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BaseSequence

__all__ = ["SubSequence"]

class SubSequence(BaseSequence):
    """Configuration for sub-sequences.
    """

    name = pexConfig.Field('The identifier for the sub-sequence.', str)
    filters = pexConfig.ListField('The list of filters required for the sub-sequence.', str)
    visits_per_filter = pexConfig.ListField('The number of visits required for each filter in the '
                                            'sub-sequence.', int)

    def setDefaults(self):
        """Default specification for SubSequence information.
        """
        BaseSequence.setDefaults(self)
        self.filters = []
        self.visits_per_filter = []

    def get_filter_string(self):
        """A string representation of the filter list parameter.

        Returns
        -------
        str
        """
        return ",".join(self.filters)
