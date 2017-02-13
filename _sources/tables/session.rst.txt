.. _database-tables-session:

=======
Session
=======

This table contains the log of all simulations (MySQL) or a single simulation (SQLite). Simulation runs are identified by the combination of the hostname and session Id: *sessionHost_sessionId*.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  sessionId
      -  Numeric identifier for the current simulation instance.
    * -  sessionUser
      -  Computer username of the simulation runner.
    * -  sessionHost
      -  Computer hostname where the simulation was run.
    * -  sessionDate
      -  The UTC date/time of the simulation start.
    * -  version
      -  The version number of the SOCS code.
    * -  runComment
      -  A description of the simulation setup.
