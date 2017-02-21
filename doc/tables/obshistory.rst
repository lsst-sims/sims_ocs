.. _database-tables-obshistory:

==========
ObsHistory
==========

This table keeps a record of each visit made by the observatory during a simulated survey. Multiple proposals can be associated with a single visit leading to duplicate entries in this table.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  observationId
      -  Numeric identifier for an observation entry.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  night
      -  The night in the survey for the observation. Starts from 1.
    * -  observationStartTime
      -  The UTC start time for the observation (units=seconds). This occurs after the slew but before the first exposure.
    * -  observationStartMJD
      -  The Modified Julian Date at observation start (units=seconds).
    * -  observationStartLST
      -  The Local Sidereal Time at observation start (units=degrees)
    * -  TargetHistory_targetId
      -  Numeric identifier that relates to an entry in the TargetHistory entry.
    * -  Field_fieldId
      -  Numeric identifier that relates to an entry in the Field table.
    * -  groupId
      -  Group Id for the observation. This is non-zero and repeated for field/filter combinations collected in sets of N (tuples or sequences). It is zero when N equal one.
    * -  filter
      -  The one character name for the band filter.
    * -  ra
      -  The Right Ascension of the observation (units=degrees).
    * -  dec
      -  The Declination of the observation (units=degrees).
    * -  angle
      -  The Position Angle of the observation (units=degrees).
    * -  altitude
      -  The altitude of the observation (units=degrees).
    * -  azimuth
      -  The azimuth of the observation (units=degrees)
    * -  numExposures
      -  The number of exposures taken for the observation.
    * -  visitTime
      -  The total time for the observation (units=seconds) including exposure, shutter and readout time.
    * -  visitExposureTime
      -  The sum of all the exposure times for the observation (units=seconds). No shutter and readout time included.
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
    * -  fiveSigmaDepth
      -  The magnitude of a point source that would be a 5-sigma detection (units=magnitudes)
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
    * -  sunRA
      -  The right-ascension (units=degrees) of the sun.
    * -  sunDec
      -  The declination (units=degrees) of the sun.
    * -  sunAlt
      -  The altitude (units=degrees) of the sun.
    * -  sunAz
      -  The azimuth (units=degrees) of the sun.
    * -  solarElong
      -  The solar elongation (units=degrees) of the observation field (distance between it and sun).
