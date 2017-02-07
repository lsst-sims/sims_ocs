import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import BaseSequence, SubSequence

__all__ = ["MasterSubSequence"]

class MasterSubSequence(BaseSequence):
    """Configuration for master sub-sequences.
    """

    name = pexConfig.Field('The identifier for the master sub-sequence.', str)
    sub_sequences = pexConfig.ConfigDictField('The set of nested sub-sequences for this master sub-sequence.',
                                              int, SubSequence)

    def setDefaults(self):
        """Default specification for MasterSubSequence information.
        """
        BaseSequence.setDefaults(self)
