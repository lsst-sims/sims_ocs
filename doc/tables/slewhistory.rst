.. _database-tables-slewhistory:

===========
SlewHistory
===========

This table contains the basic slew information for each visit.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  slewCount
      -  Numeric identifier for a particular slew.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  startDate
      -  The UTC date for the start of the slew (units=seconds).
    * -  endDate
      -  The UTC date for the end of the slew (units=seconds).
    * -  slewTime
      -  The duration of the slew (units=seconds).
    * -  slewDistance
      -  The angular distance traveled on the sky of the slew (units=degrees).
    * -  ObsHistory_observationId
      -  Numeric identifier that relates to an entry in the ObsHistory table.
