.. _database-tables-obsexposures:

============
ObsExposures
============

This table contains all of the individual exposure information for each visit in the :ref:`database-tables-obshistory` table. The number of exposures in a visit is determined by the visit target's exposure cadence.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  exposureId
      -  Numeric identifier for an observation exposure.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  exposureNum
      -  The order number of the exposure. Starts at 1 for a set of exposures.
    * -  exposureStartTime
      -  The UTC start time of the particular exposure (units=seconds).
    * -  exposureTime
      -  The duration of the exposure (units=seconds).
    * -  ObsHistory_observationId
      -  Numeric identifier that relates to an entry in the ObsHistory table.
