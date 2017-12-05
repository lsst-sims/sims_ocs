from __future__ import division
from builtins import object
from datetime import datetime
import numpy
import os
import sqlite3

__all__ = ["SeeingModel"]


class SeeingModel(object):
    """Handle the seeing information.

    This class deals with the seeing information that was previously produced for
    OpSim version 3.
    """

    SEEING_DB = "seeing.db"
    """Filename of the internal seeing observation database."""
    AIRMASS_CORRECTION_POWER = 0.6
    FILTER_WAVELENGTH_CORRECTION_POWER = 0.3
    RAW_SEEING_WAVELENGTH = 500  # nm

    def __init__(self, time_handler):
        """Initialize the class.

        Parameters
        ----------
        time_handler : :class:`.TimeHandler`
            The instance of the simulation time handler.
        """
        self.seeing_db = None
        self.seeing_dates = None
        self.seeing_values = None
        self.environment_config = None
        self.filters_config = None
        self.filter_wavelength_correction = {}
        model_time_start = datetime(time_handler.initial_dt.year, 1, 1)
        self.offset = time_handler.time_since_given_datetime(model_time_start,
                                                             reverse=True)

    def calculate_seeing(self, delta_time, filter_name, airmass):
        """Calculate the geometric and effective seeing values.

        Parameters
        ----------
        delta_time : int
            The time (seconds) from the start of the simulation.
        filter_name : str
            The single character filter name for the calculation.
        airmass : float
            The airmass for the calculation.

        Returns
        -------
        tuple
            The FWHM 500nm, FWHM Geometric and FWHM Effective seeing values.
        """
        if filter_name == '':
            return (-1.0, -1.0, -1.0)
        fwhm_500 = self.get_seeing(delta_time)
        airmass_correction = numpy.power(airmass, self.AIRMASS_CORRECTION_POWER)
        try:
            filter_wavelength_correction = self.filter_wavelength_correction[filter_name]
        except KeyError:
            # Then add this new filter to our dictionary, and remember it for next time.
            filter_wavelength = self.filters_config.get_effective_wavelength(filter_name)
            filter_wavelength_correction = numpy.power(self.RAW_SEEING_WAVELENGTH / filter_wavelength,
                                                       self.FILTER__WAVELENGTH_CORRECTION_POWER)
            self.filter_wavelength_correction[filter_name] = filter_wavelength_correction

        seeing_fwhm_system = numpy.sqrt((self.environment_config.telescope_seeing * airmass_correction)**2 +
                                        self.environment_config.optical_design_seeing**2 +
                                        self.environment_config.camera_seeing**2)
        seeing_fwhm_atmos = fwhm_500 * filter_wavelength_correction * airmass_correction
        fwhm_effective = (self.environment_config.scale_to_eff *
                          numpy.sqrt(seeing_fwhm_system**2 +
                                     self.environment_config.geom_eff_factor * seeing_fwhm_atmos**2))
        fwhm_geometric = 0.822 * fwhm_effective + 0.052   # from sims_photUtils instead in future?

        return (fwhm_500, fwhm_geometric, fwhm_effective)

    def get_seeing(self, delta_time):
        """Get the seeing for the specified time.

        Parameters
        ----------
        delta_time : int
            The time (seconds) from the start of the simulation.

        Returns
        -------
        float
            The seeing (arcseconds) closest to the specified time.
        """
        delta_time += self.offset
        date = delta_time % self.seeing_dates[-1]
        idx = numpy.searchsorted(self.seeing_dates, date)
        # searchsorted ensures that left < date < right
        # but we need to know if date is closer to left or to right
        left = self.seeing_dates[idx - 1]
        right = self.seeing_dates[idx]
        if date - left < right - date:
            idx -= 1
        return self.seeing_values[idx]

    def initialize(self, environment_config, filters_config):
        """Configure the seeing information.

        This function gets the environment and filters configuration
        and creates the seeing information from the appropriate database.
        The default behavior is to use the module stored database. However, an
        alternate database file can be provided. The alternate database file needs to have a
        table called *Seeing* with the following columns:

        seeingId
            int : A unique index for each seeing entry.
        s_date
            int : The time (units=seconds) since the start of the simulation for the seeing observation.
        seeing
            float : The FWHM of the atmospheric PSF (units=arcseconds).

        Parameters
        ----------
        environment_config : :class:`.Environment`
            The configuration instance for the environment.
        filters_config : :class:`.Filters`
            The configuration instance for the filters.
        """
        self.environment_config = environment_config
        self.filters_config = filters_config

        if self.environment_config.seeing_db != "":
            self.seeing_db = self.environment_config.seeing_db
        else:
            self.seeing_db = os.path.join(os.path.dirname(__file__), self.SEEING_DB)

        with sqlite3.connect(self.seeing_db) as conn:
            cur = conn.cursor()
            query = "select s_date, seeing from Seeing order by s_date;"
            cur.execute(query)
            results = numpy.array(cur.fetchall())
            self.seeing_dates = numpy.hsplit(results, 2)[0].flatten()
            self.seeing_values = numpy.hsplit(results, 2)[1].flatten()
            cur.close()

    def set_topic(self, th, topic):
        """Set the seeing information into the topic.

        Parameters
        ----------
        th : :class:`.TimeHandler`
            A time hadnling instance.
        topic : SALPY_scheduler.scheduler_seeingC
            An instance of the seeing topic.
        """
        topic.timestamp = th.current_timestamp
        topic.seeing = self.get_seeing(th.time_since_start)
