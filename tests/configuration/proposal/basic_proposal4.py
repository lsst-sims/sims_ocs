from lsst.sims.ocs.configuration.proposal import General, GeneralBandFilter, Selection
from lsst.sims.ocs.configuration.proposal import SelectionList, TimeRange
from lsst.sims.ocs.configuration.proposal import SELECTION_LIMIT_TYPES

class BasicProposal4(General):
    """This class sets the parameters for specifying a test proposal.
    """

    def setDefaults(self):
        """Setup all the proposal information.
        """
        self.name = "BasicProposal4"

        # -------------------------
        # Sky Region specifications
        # -------------------------

        # Dec Band 1
        dec_limit1 = Selection()
        dec_limit1.limit_type = SELECTION_LIMIT_TYPES[1]
        dec_limit1.minimum_limit = -60
        dec_limit1.maximum_limit = -30

        # Dec Band 2
        dec_limit2 = Selection()
        dec_limit2.limit_type = SELECTION_LIMIT_TYPES[1]
        dec_limit2.minimum_limit = -30
        dec_limit2.maximum_limit = 0

        self.sky_region.selections = {0: dec_limit1, 1: dec_limit2}

        # Set time ordering information
        # Dec Band 1
        time_range1 = TimeRange()
        time_range1.start = 1
        time_range1.end = 1825

        # Dec Band 2
        time_range2 = TimeRange()
        time_range2.start = 1826
        time_range2.end = 3650

        self.sky_region.time_ranges = {0: time_range1, 1: time_range2}

        # Set selection mapping information
        # Dec Band 1
        selection_list1 = SelectionList()
        selection_list1.indexes = [0]

        # Dec Band 2
        selection_list2 = SelectionList()
        selection_list2.indexes = [1]

        self.sky_region.selection_mapping = {0: selection_list1, 1: selection_list2}

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
        self.scheduling.restrict_grouped_visits = False
        self.scheduling.time_interval = 30 * 60
        self.scheduling.time_window_start = -0.5
        self.scheduling.time_window_max = 0.5
        self.scheduling.time_window_end = 1.0
        self.scheduling.time_weight = 1.0

        # --------------------------
        # Band Filter specifications
        # --------------------------

        u_filter = GeneralBandFilter()
        u_filter.name = 'u'
        u_filter.num_visits = 75
        u_filter.num_grouped_visits = 1
        u_filter.bright_limit = 21.0
        u_filter.dark_limit = 30.0
        u_filter.max_seeing = 1.5
        u_filter.exposures = [15.0, 15.0]

        g_filter = GeneralBandFilter()
        g_filter.name = 'g'
        g_filter.num_visits = 105
        g_filter.num_grouped_visits = 2
        g_filter.bright_limit = 21.0
        g_filter.dark_limit = 30.0
        g_filter.max_seeing = 1.5
        g_filter.exposures = [15.0, 15.0]

        r_filter = GeneralBandFilter()
        r_filter.name = 'r'
        r_filter.num_visits = 240
        r_filter.num_grouped_visits = 2
        r_filter.bright_limit = 20.25
        r_filter.dark_limit = 30.0
        r_filter.max_seeing = 1.5
        r_filter.exposures = [15.0, 15.0]

        i_filter = GeneralBandFilter()
        i_filter.name = 'i'
        i_filter.num_visits = 240
        i_filter.num_grouped_visits = 2
        i_filter.bright_limit = 19.5
        i_filter.dark_limit = 30.0
        i_filter.max_seeing = 1.5
        i_filter.exposures = [15.0, 15.0]

        self.filters = {u_filter.name: u_filter,
                        g_filter.name: g_filter,
                        r_filter.name: r_filter,
                        i_filter.name: i_filter}
