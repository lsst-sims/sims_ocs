import lsst.pex.config as pexConfig

__all__ = ["Camera"]

class Camera(pexConfig.Config):
    """Configuration of the LSST Camera.
    """

    readout_time = pexConfig.Field('Time (units=seconds) for the camera electronics readout.', float)
    shutter_time = pexConfig.Field('Time (units=seconds) for the camera shutter to open or close', float)

    # Filter parameters
    filter_mount_time = pexConfig.Field('Time (units=seconds) to mount a filter.', float)
    filter_change_time = pexConfig.Field('Time (units=seconds) to change a filter.', float)
    filter_max_changes_burst_num = pexConfig.Field('Maximum number of filter changes in a night.', int)
    filter_max_changes_burst_time = pexConfig.Field('Minimum time (units=seconds) between filter changes '
                                                    'in a night.', float)
    filter_max_changes_avg_num = pexConfig.Field('Maximum average number of filter changes per year.', int)
    filter_max_changes_avg_time = pexConfig.Field('Maximum time (units=seconds) for the average number of '
                                                  'filter changes.', float)

    filter_mounted = pexConfig.ListField('Initial state for the mounted filters. Empty positions must be '
                                         'filled with id="" no (filter).', str)
    filter_pos = pexConfig.Field('The currently mounted filter.', str)
    filter_removable = pexConfig.ListField('The list of filters that can be removed.', str)
    filter_unmounted = pexConfig.ListField('The list of unmounted but available to swap filters.', str)

    def setDefaults(self):
        """Set defaults for the LSST Camera.
        """
        self.readout_time = 2.0
        self.shutter_time = 1.0
        self.filter_mount_time = 8 * 3600.0
        self.filter_change_time = 120.0
        self.filter_max_changes_burst_num = 1
        self.filter_max_changes_burst_time = 0 * 60.0
        self.filter_max_changes_avg_num = 3000
        self.filter_max_changes_avg_time = 365.25 * 24.0 * 60.0 * 60.0
        self.filter_mounted = ['g', 'r', 'i', 'z', 'y']
        self.filter_pos = 'r'
        self.filter_removable = ['y', 'z']
        self.filter_unmounted = ['u']

    @property
    def filter_mounted_str(self):
        """str: The list of mounted filters.
        """
        return ",".join(self.filter_mounted)

    @property
    def filter_removable_str(self):
        """str: The list of filters that can be removed.
        """
        return ",".join(self.filter_removable)

    @property
    def filter_unmounted_str(self):
        """str: The list of unmounted filters.
        """
        return ",".join(self.filter_unmounted)
