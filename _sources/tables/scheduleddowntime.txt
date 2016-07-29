.. _database-tables-scheduleddowntime:

=================
ScheduledDowntime
=================

This table records all of the scheduled downtime for the entire survey (plus an extra 10 years). The actual downtime used in the simulation maybe different depending on the length of the simulation.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  night
      -  The starting night for the downtime.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  duration
      -  The length of the downtime (units=days).
    * -  activity
      -  The description of the activity associated with the downtime.
