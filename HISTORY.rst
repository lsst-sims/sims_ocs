.. :changelog:

History
-------

0.3 (2016-05-20)
~~~~~~~~~~~~~~~~

Next interim release of SOCS. Focused on performing observations and handling area 
distribution proposals.

* More information to survey data base

  * All slew related information: SlewHistory, InitialSlewState, FinalSlewState, SlewMaxSpeeds and SlewActivities
  * More information to TargetHistory and ObsHistory tables
  * New tables (TargetExposures and ObservationExposures) for tracking exposure cadences

* Implemented configuration for area distribution proposals

* Observation cycle

  * Use real night boundaries to drive simulation
  * Slew SOCS Observatory model to target from Scheduler
  * Calculate visit time from exposure cadence
  * Passing Observatory state back to Scheduler

* Create system to log information to a central file from both SOCS and Scheduler

* Implemented simple variational model for Observatory model

  * Percent change degradation
  * Only effects telescope and dome accelerations and speeds

0.2 (2015-12-30)
~~~~~~~~~~~~~~~~

Initial release of SOCS in conjunction with the Scheduler.  Focused on infrastructure and basic observation loop.

* Implemented SAL interaction layer

* Created the initial driver script

* Implemented configuration system
  
  * Survey, Scheduler, Site and Observatory configurations implemented
  * Communication of configuration via SAL to Scheduler implemented

* Implement DB interaction layer with MySQL and SQLite options

  * Session, Field, TargetHistory and ObsHistory tables implemented
  * Created script to aid in database setup

* Implemented main class to drive the full simulation

  * Start and end of simulation operations
  * Start and end of night operations
  * Basic target-observation cycle
  * Communication of configuration, timestamp, targets and observations to Scheduler

* Implemented time handler for simulation time

* Implemented sequencer to perform the observation task

* Implemented SOCS Observatory via aggregation from Scheduler Observatory model