.. _database-tables-summaryallprops:

===============
SummaryAllProps
===============

This table contains a summary set of information from the observations by joining
certain columns from particular tables. There is one row for each proposal observed
target. If more that one proposal received the same observation, rows with mostly 
duplicated information, except proposal Id, are created.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  observationId
      -  Numeric identifier for an observation entry.
    * -  night
      -  The night in the survey for the observation. Starts from 1.
    * -  observationStartTime
      -  The UTC start time for the observation (units=seconds). This occurs after the slew but before the first exposure.
    * -  observationStartMJD
      -  The Modified Julian Date at observation start (units=seconds).
    * -  observationStartLST
      -  The Local Sidereal Time at observation start (units=degrees)
    * -  numExposures
      -  The number of exposures taken for the observation.
    * -  visitTime
      -  The total time for the observation (units=seconds) including exposure, shutter and readout time.
    * -  visitExposureTime
      -  The sum of all the exposure times for the observation (units=seconds). No shutter and readout time included.
    * -  proposalId
      -  Numeric identifier that relates to an entry in the Proposal table.
    * -  filter
      -  The one character name for the band filter.
    * -  altitude
      -  The altitude of the observation (units=degrees).
    * -  azimuth
      -  The azimuth of the observation (units=degrees)
    * -  airmass
      -  The airmass of the observation field.
    * -  skyBrightness
      -  The calculated skybrightness for the observation field.
    * -  cloud
      -  The fraction of clouds present (0: none to 1: total).
    * -  seeingFwhm500
      -  The full-width at half-maximum for seeing observations at 500 nm at zenith.
    * -  seeingFwhmGeom
      -  "Geometrical" full-width at half-maximum, actual half width at maximum brightness. This can be used to represent the FWHM of a double Gaussian representing the physical width of a PSF.
    * -  seeingFwhmEff
      -  "Effective" full-width at half-maximum, typically ~15% larger than seeingFwhmGeom. This can be used to calculate SNR for point sources, using seeingFwhmEff as the FWHM of a single Gaussian describing the PSF.
    * -  slewTime
      -  The duration of the slew (units=seconds).
    * -  slewDistance
      -  The angular distance traveled on the sky of the slew (units=degrees).
    * -  paraAngle
      -  Current parallactic angle of the rotator (units=degrees).
    * -  rotTelPos
      -  Current position of the telescope rotator (units=degrees).
    * -  rotSkyPos
      -  Current position of the camera on the sky (units=degrees).
    * -  moonRA
      -  The right-ascension (units=degrees) of the moon.
    * -  moonDec
      -  The declination (units=degrees) of the moon.
    * -  moonAlt
      -  The altitude (units=degrees) of the moon.
    * -  moonAz
      -  The azimuth (units=degrees) of the moon.
    * -  moonDistance
      -  The distance (units=degrees) between the moon and the observation field.
    * -  moonPhase
      -  The phase of the moon.
    * -  sunAlt
      -  The altitude (units=degrees) of the sun.
    * -  sunAz
      -  The azimuth (units=degrees) of the sun.
    * -  solarElong
      -  The solar elongation (units=degrees) of the observation field (distance between it and sun).
