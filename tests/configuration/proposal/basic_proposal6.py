from lsst.sims.ocs.configuration.proposal import BandFilter, MasterSubSequence, SubSequence, Sequence

class BasicProposal6(Sequence):
    """This class sets the parameters for specifying a test proposal.
    """

    def setDefaults(self):
        """Setup all the proposal information.
        """
        self.name = "BasicProposal6"

        # -------------------------
        # Sky Region specifications
        # -------------------------

        self.sky_user_regions = [597, 1486, 2206]

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

        #----------------------------
        # Sub-Sequence specifications
        #----------------------------

        # No stand alone sub-sequences

        #----------------------------------------------
        # Master and Nested Sub-Sequence specifications
        #----------------------------------------------

        msseq0 = MasterSubSequence()
        msseq0.name = "master0"
        msseq0.num_events = 20
        msseq0.num_max_missed = 5
        msseq0.time_interval = 3 * 24 * 60 * 60
        msseq0.time_window_start = 0.0
        msseq0.time_window_max = 1.0
        msseq0.time_window_end = 2.0
        msseq0.time_weight = 1.0

        sseq0 = SubSequence()
        sseq0.name = "Only_GR"
        sseq0.filters = ['g', 'r']
        sseq0.visits_per_filter = [2, 2]
        sseq0.num_events = 5
        sseq0.num_max_missed = 0
        sseq0.time_interval = 2 * 60 * 60
        sseq0.time_window_start = 0.0
        sseq0.time_window_max = 1.0
        sseq0.time_window_end = 2.0
        sseq0.time_weight = 1.0

        msseq0.sub_sequences = {0: sseq0}

        msseq1 = MasterSubSequence()
        msseq1.name = "master1"
        msseq1.num_events = 25
        msseq1.num_max_missed = 5
        msseq1.time_interval = 5 * 24 * 60 * 60
        msseq1.time_window_start = 0.0
        msseq1.time_window_max = 1.0
        msseq1.time_window_end = 2.0
        msseq1.time_weight = 1.0

        sseq1 = SubSequence()
        sseq1.name = "Only_IZ"
        sseq1.filters = ['i', 'z']
        sseq1.visits_per_filter = [1, 1]
        sseq1.num_events = 10
        sseq1.num_max_missed = 1
        sseq1.time_interval = 6 * 60 * 60
        sseq1.time_window_start = 0.0
        sseq1.time_window_max = 1.0
        sseq1.time_window_end = 2.0
        sseq1.time_weight = 1.0

        msseq1.sub_sequences = {0: sseq1}

        self.master_sub_sequences = {0: msseq0, 1: msseq1}

        # ----------------------
        # Scheduling information
        # ----------------------

        self.scheduling.max_num_targets = 100
        self.scheduling.accept_serendipity = False
        self.scheduling.accept_consecutive_visits = True
        self.scheduling.restart_complete_sequences = False

        # --------------------------
        # Band Filter specifications
        # --------------------------

        u_filter = BandFilter()
        u_filter.name = 'u'
        u_filter.bright_limit = 21.0
        u_filter.dark_limit = 30.0
        u_filter.max_seeing = 1.5
        u_filter.exposures = [15.0, 15.0]

        g_filter = BandFilter()
        g_filter.name = 'g'
        g_filter.bright_limit = 21.0
        g_filter.dark_limit = 30.0
        g_filter.max_seeing = 1.5
        g_filter.exposures = [15.0, 15.0]

        r_filter = BandFilter()
        r_filter.name = 'r'
        r_filter.bright_limit = 20.25
        r_filter.dark_limit = 30.0
        r_filter.max_seeing = 1.5
        r_filter.exposures = [15.0, 15.0]

        i_filter = BandFilter()
        i_filter.name = 'i'
        i_filter.bright_limit = 19.5
        i_filter.dark_limit = 30.0
        i_filter.max_seeing = 1.5
        i_filter.exposures = [15.0, 15.0]

        self.filters = {u_filter.name: u_filter,
                        g_filter.name: g_filter,
                        r_filter.name: r_filter,
                        i_filter.name: i_filter}
