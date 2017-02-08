.. _database-tables-slewmaxspeeds:

=============
SlewMaxSpeeds
=============

This table contains all of the maximum speeds obtained by the telescope, dome and rotator during a given visit's slew. The *SlewHistory_slewCount* column points to a given slew in the :ref:`database-tables-slewhistory` table.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  slewMaxSpeedId
      -  Numeric identifier for a particular slew max speeds entry.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  domeAltSpeed
      -  The maximum dome altitude speed achieved during the slew (units=degrees/second).
    * -  domeAzSpeed
      -  The maximum dome azimuth speed achieved during the slew (units=degrees/second).
    * -  telAltSpeed
      -  The maximum telescope altitude speed achieved during the slew (units=degrees/second).
    * -  telAzSpeed
      -  The maximum telescope azimuth speed achieved during the slew (units=degrees/second).
    * -  rotatorSpeed
      -  The maximum rotator speed achieved during the slew (units=degrees/second).
    * -  SlewHistory_slewCount
      -  Numeric identifier that relates to an entry in the SlewHistory table.
