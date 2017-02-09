.. _database-tables-slewactivities:

==============
SlewActivities
==============

This table contains all the activities for a given visit's slew. The *SlewHistory_slewCount* column points to a given slew in the :ref:`database-tables-slewhistory` table.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  slewActivityId
      -  Numeric identifier for a particular slew activity entry.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  activity
      -  Short description of the slew activity.
    * -  activityDelay
      -  The delay time of the slew activity (units=seconds).
    * -  inCriticalPath
      -  True is slew activity is in the critical path and False if not.
    * -  SlewHistory_slewCount
      -  Numeric identifier that relates to an entry in the SlewHistory table.
