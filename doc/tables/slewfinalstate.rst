.. _database-tables-slewfinalstate:

==============
SlewFinalState
==============

This table contains all of the final state information from a given visit's slew. The state information is collected after the slew has completed, but before the visit activity has started. The *SlewHistory_slewCount* column points to a given slew in the :ref:`database-tables-slewhistory` table.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  slewStateId
      -  Numeric identifier for a particular slew state.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  slewStateDate
      -  The UTC date/time of the slew state information (units=seconds)
    * -  targetRA
      -  Current target Right Ascension (units=degrees).
    * -  targetDec
      -  Current target Declination (units=degrees).
    * -  tracking
      -  Whether or not the telescope is tracking the sky.
    * -  altitude
      -  Current target altitude (units=degrees).
    * -  azimuth
      -  Current target azimuth (units=degrees)
    * -  paraAngle
      -  Current parallactic angle of the rotator (units=degrees).
    * -  domeAlt
      -  Current dome altitude (units=degrees).
    * -  domeAz
      -  Current dome azimuth (units=degrees).
    * -  telAlt
      -  Current telescope altitude (units=degrees).
    * -  telAz
      -  Current telescope azimuth (units=degrees).
    * -  rotTelPos
      -  Current position of the telescope rotator (units=degrees).
    * -  rotSkyPos
      -  Current position of the camera on the sky (units=degrees).
    * -  filter
      -  Band filter for the recorded slew state.
    * -  SlewHistory_slewCount
      -  Numeric identifier that relates to an entry in the SlewHistory table.
