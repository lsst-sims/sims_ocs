.. _database-tables-targetexposures:

===============
TargetExposures
===============

This table contains all of the individual exposure information for each target in the :ref:`database-tables-targethistory` table. The number of exposures for a target is determined by the requesting proposal's exposure cadence.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  exposureId
      -  Numeric identifier for a particular target exposure.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  exposureNum
      -  The order number of the exposure. Starts at 1 for a set of exposures.
    * -  exposureTime
      -  The requested duration of the exposure (units=seconds).
    * -  TargetHistory_targetId
      -  Numeric identifier that relates to an entry in the TargetHistory table.
