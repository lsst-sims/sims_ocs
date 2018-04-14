from __future__ import division
from builtins import object
from datetime import datetime
import numpy
import os
import sqlite3

from lsst.sims.seeingModel import SeeingSim

__all__ = ["SeeingInterface"]


class SeeingInterface(object):
    """Interface between SOCS and the SeeingSim.

    This class deals with interaction to the CloudModel as well as topic handling
    for it.
    """

    def __init__(self, time_handler):
        """Initialize the class.

        Parameters
        ----------
        time_handler : :class:`.TimeHandler`
            The instance of the simulation time handler.
        """
        self.time_handler = time_handler

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
        return self.seeingSim.get_seeing_singlefilter(delta_time, filter_name, airmass)

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
        return self.seeingSim.get_fwhm500(delta_time)

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
        seeing_db = environment_config.seeing_db
        if seeing_db == "":
            seeing_db = None

        self.seeingSim = SeeingSim(self.time_handler, seeing_db=seeing_db,
                                   telescope_seeing=environment_config.telescope_seeing,
                                   optical_design_seeing=environment_config.optical_design_seeing,
                                   camera_seeing=environment_config.camera_seeing)

        self.environment_config = environment_config


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
