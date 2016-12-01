from lsst.sims.ocs.configuration.proposal import General, BandFilter, Selection
from lsst.sims.ocs.configuration.proposal import SELECTION_LIMIT_TYPES

class BasicProposal2(General):
    """This class sets the parameters for specifying a test proposal.
    """

    def setDefaults(self):
        """Setup all the proposal information.
        """
        self.name = "BasicProposal2"

        # -------------------------
        # Sky Region specifications
        # -------------------------

        # Dec Band
        dec_limit = Selection()
        dec_limit.limit_type = SELECTION_LIMIT_TYPES[1]
        dec_limit.minimum_limit = -50
        dec_limit.maximum_limit = -20

        # RA Band
        ra_limit = Selection()
        ra_limit.limit_type = SELECTION_LIMIT_TYPES[0]
        ra_limit.minimum_limit = 45.0
        ra_limit.maximum_limit = 90.0

        self.sky_region.selections = {0: dec_limit, 1: ra_limit}

        # Combine the Dec and RA bands
        self.sky_region.combiners = ["and"]

        # -----------------------------
        # Sky Exclusion specifications
        # -----------------------------

        self.sky_exclusion.dec_window = 90.0

        # ---------------------------------
        # Sky Nightly Bounds specifications
        # ---------------------------------

        self.sky_nightly_bounds.twilight_boundary = -12.0
        self.sky_nightly_bounds.delta_lst = 60.0

        # ------------------------------
        # Sky Constraints specifications
        # ------------------------------

        self.sky_constraints.max_airmass = 2.5

        # ----------------------
        # Scheduling information
        # ----------------------

        self.scheduling.max_num_targets = 100
        self.scheduling.accept_serendipity = False
        self.scheduling.accept_consecutive_visits = False

        # --------------------------
        # Band Filter specifications
        # --------------------------

        g_filter = BandFilter()
        g_filter.name = 'g'
        g_filter.num_visits = 105
        g_filter.bright_limit = 21.0
        g_filter.dark_limit = 30.0
        g_filter.max_seeing = 1.5
        g_filter.exposures = [15.0, 15.0]

        r_filter = BandFilter()
        r_filter.name = 'r'
        r_filter.num_visits = 240
        r_filter.bright_limit = 20.25
        r_filter.dark_limit = 30.0
        r_filter.max_seeing = 1.5
        r_filter.exposures = [15.0, 15.0]

        i_filter = BandFilter()
        i_filter.name = 'i'
        i_filter.num_visits = 240
        i_filter.bright_limit = 19.5
        i_filter.dark_limit = 30.0
        i_filter.max_seeing = 1.5
        i_filter.exposures = [15.0, 15.0]

        self.filters = {g_filter.name: g_filter,
                        r_filter.name: r_filter,
                        i_filter.name: i_filter}
