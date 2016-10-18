import lsst.pex.config as pexConfig

__all__ = ["Filters"]

class Filters(pexConfig.Config):
    """Configuration of the LSST filters.
    """

    u_effective_wavelength = pexConfig.Field('The effective wavelength (units=nm) for the u filter '
                                             'calculated from the throughputs.', float)
    g_effective_wavelength = pexConfig.Field('The effective wavelength (units=nm) for the g filter '
                                             'calculated from the throughputs.', float)
    r_effective_wavelength = pexConfig.Field('The effective wavelength (units=nm) for the r filter '
                                             'calculated from the throughputs.', float)
    i_effective_wavelength = pexConfig.Field('The effective wavelength (units=nm) for the i filter '
                                             'calculated from the throughputs.', float)
    z_effective_wavelength = pexConfig.Field('The effective wavelength (units=nm) for the z filter '
                                             'calculated from the throughputs.', float)
    y_effective_wavelength = pexConfig.Field('The effective wavelength (units=nm) for the y filter '
                                             'calculated from the throughputs.', float)

    def setDefaults(self):
        """Set defaults for the LSST Filters.
        """
        self.u_effective_wavelength = 367.0
        self.g_effective_wavelength = 482.5
        self.r_effective_wavelength = 622.2
        self.i_effective_wavelength = 754.5
        self.z_effective_wavelength = 869.1
        self.y_effective_wavelength = 971.0

    def get_effective_wavelength(self, filter_name):
        """Get the effective wavelength for a given filter.

        Parameters
        ----------
        filter_name : str
            The single character name of the filter.

        Returns
        -------
        float
            The effective wavelength (nm) of the given filter.
        """
        return getattr(self, "{}_effective_wavelength".format(filter_name))
