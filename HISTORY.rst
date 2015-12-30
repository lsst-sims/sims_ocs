.. :changelog:

History
-------

0.2 (2015-12-30)
~~~~~~~~~~~~~~~~

Initial release of SOCS in conjunction with the Scheduler.  Focused on infrastructure and basic observation loop.

* Implemented SAL interaction layer

* Created the initial driver script

* Implemented configuration system
  
  * Survey, Scheduler, Site and Observatory configurations implemented
  * Communcation of configuration via SAL to Scheduler implemented

* Implement DB interaction layer with MySQL and SQLite options

  * Session, Field, TargetHistory and ObsHistory tables implemented
  * Created script to aid in database setup

* Implemented main class to drive the full simulation

  * Start and end of simulation operations
  * Start and end of night operations
  * Basic target-observation cycle
  * Communcation of configuration, timestamp, targets and observations to Scheduler

* Implemented time handler for simulation time

* Implemented sequencer to perform the observation task

* Implemented SOCS Observatory via aggregation from Scheduler Observatory model