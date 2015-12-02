import lsst.pex.config as pexConfig

__all__ = ["Camera"]

class Camera(pexConfig.Config):
    """Configuration of the LSST Camera.
    """

    readout_time = pexConfig.Field('Time (units=seconds) for the camera electronics readout.', float)
    shutter_time = pexConfig.Field('Time (units=seconds) for the camera shutter to open or close', float)

    # Filter parameters
    filter_mounttime = pexConfig.Field('Time (units=seconds) to mount a filter.', float)
    filter_movetime = pexConfig.Field('Time (units=seconds) to move a filter.', float)

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
        self.filter_mounttime = 8 * 3600.0
        self.filter_movetime = 120.0
        self.filter_mounted = ['g', 'r', 'i', 'z', 'y']
        self.filter_pos = 'r'
        self.filter_removable = ['y', 'z']
        self.filter_unmounted = ['u']
