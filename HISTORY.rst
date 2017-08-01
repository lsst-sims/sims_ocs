.. :changelog:

History
-------

1.0.8 (2017-08-01)
~~~~~~~~~~~~~~~~~~

* Speed improvement for cloud and seeing lookup (from dhroth)
* New configuration parameters

  * propboost_weight in SchedulerDriver
  * max_visits_goal in Sequence

* Fix handling of null target when first target
* Fix to stack installation directions

1.0.7 (2017-06-19)
~~~~~~~~~~~~~~~~~~

* Fix crash when saving configuration with only one type of proposal present
* Synchronize timeouts between SOCS and Scheduler when greater than 180 seconds

1.0.6 (2017-06-14)
~~~~~~~~~~~~~~~~~~

* Extended exception handling in driver script to catch startup issues
* Cleaned up linting errors

1.0.5 (2017-06-07)
~~~~~~~~~~~~~~~~~~

* Baseline parameter changes

  * SchedulerDriver.timecost_cost_ref = 0.3 

1.0.4 (2017-06-06)
~~~~~~~~~~~~~~~~~~

* Added ProposalField table to survey database
* Fields no longer received from Scheduler, internally generated
* Baseline parameter changes

  * WideFastDeep.max_num_targets = 500
  * Park.filter_position = z
  * SchedulerDriver.timecost_cost_ref = 0.03 

1.0.3 (2017-05-30)
~~~~~~~~~~~~~~~~~~

* Using new standalone packages for observatory and astronomical sky models
* Allow SOCS to provide Scheduler with different timeouts
* Handling override parameters to newly introduced proposals

1.0.2 (2017-04-20)
~~~~~~~~~~~~~~~~~~

* Handling restart lost and complete sequences parameters for Sequence proposals
* Ensuring cloud and seeing models have concept of year
* Log OSPL_URI to file

1.0.1 (2017-03-31)
~~~~~~~~~~~~~~~~~~

* Fixed Deep Drilling Cosmology 1 time window parameters
* Changed survey start date to 2022-10-01
* Fixed session tracking issue

1.0 (2017-02-28)
~~~~~~~~~~~~~~~~~

This release of SOCS is designed to replace version 3 of the Operations Simulator.

* Science proposals implemented:

  * Wide-Fast-Deep
  * North Ecliptic Spur
  * Galactic Plane
  * South Celestial Pole
  * Deep Drilling Cosmology 1

* Science proposals can be configured to have time dependent sky region selections

* Implement interested proposal behavior

* Filter swapping during dark time around new moon

* Environment information used in simulation

  * Cloud information from OpSim3 read and sent to Scheduler
  * Seeing information from OpSim3 read and sent to Scheduler, new seeing calculations added and stored to survey database

* Downtime system

  * Scheduled downtime information in small SQLite DB
  * Unscheduled downtime generated on fly using a fixed seed via algorithm

* More information to survey database

  * New tables (ObsProposalHistory, TargetProposalHistory) for tracking proposal history for observations and targets
  * More information to ObsHistory and TargetHistory tables
  * New table (Config) for tracking simulation configuration information
  * New table (Proposal) for tracking the active science proposals
  * New view (SummaryAllProps) for similar information to OpSim3 Summary table

0.3 (2016-05-20)
~~~~~~~~~~~~~~~~

Next interim release of SOCS. Focused on performing observations and handling area 
distribution proposals.

* More information to survey database

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