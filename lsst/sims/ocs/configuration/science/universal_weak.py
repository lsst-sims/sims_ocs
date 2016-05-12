from lsst.sims.ocs.configuration.proposal import AreaDistribution, BandFilter, Selection
from lsst.sims.ocs.configuration.proposal import SELECTION_LIMIT_TYPES

__all__ = ["UniversalWeak"]

class UniversalWeak(AreaDistribution):
    """This class sets the parameters for specifying the Universal Weak proposal.
    """

    def setDefaults(self):
        """Setup all the proposal information.
        """
        self.name = "UniversalWeak"

        # -------------------------
        # Sky Region specifications
        # -------------------------
        self.sky_region.twilight_boundary = -12.0
        self.sky_region.delta_lst = 60.0
        self.sky_region.dec_window = 90.0
        self.sky_region.use_galactic_exclusion = False

        # RA Band - All Sky
        ra_limit = Selection()
        ra_limit.limit_type = SELECTION_LIMIT_TYPES[0]
        ra_limit.minimum_limit = 0.0
        ra_limit.maximum_limit = 360.0

        # Dec Band
        dec_limit = Selection()
        dec_limit.limit_type = SELECTION_LIMIT_TYPES[1]
        dec_limit.minimum_limit = -60.0
        dec_limit.maximum_limit = 0.0

        self.sky_region.limit_selections = {ra_limit.limit_type: ra_limit, dec_limit.limit_type: dec_limit}

        # --------------------------
        # Band Filter specifications
        # --------------------------

        u_filter = BandFilter()
        u_filter.name = 'u'
        u_filter.num_visits = 75
        u_filter.bright_limit = 21.3
        u_filter.dark_limit = 30.0
        u_filter.max_seeing = 1.5
        u_filter.exposures = [15.0, 15.0]

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

        z_filter = BandFilter()
        z_filter.name = 'z'
        z_filter.num_visits = 210
        z_filter.bright_limit = 17.0
        z_filter.dark_limit = 21.0
        z_filter.max_seeing = 1.5
        z_filter.exposures = [15.0, 15.0]

        y_filter = BandFilter()
        y_filter.name = 'y'
        y_filter.num_visits = 210
        y_filter.bright_limit = 16.5
        y_filter.dark_limit = 21.0
        y_filter.max_seeing = 1.5
        y_filter.exposures = [15.0, 15.0]

        self.filters = {u_filter.name: u_filter,
                        g_filter.name: g_filter,
                        r_filter.name: r_filter,
                        i_filter.name: i_filter,
                        z_filter.name: z_filter,
                        y_filter.name: y_filter}

        # ----------------------
        # Scheduling information
        # ----------------------

        self.scheduling.max_num_targets = 100
        self.scheduling.accept_serendipity = False
        self.scheduling.accept_consecutive_visits = False
