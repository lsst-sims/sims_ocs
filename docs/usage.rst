========
Usage
========

The Operations Simulator consists of running the SOCS and Scheduler. Currently, they are separate scripts that must be started separately. Due to the nature of the setup, a wrapper script is recommended when launching both processes. If you have followed the installation recommendations, a highly recommended example is below.

.. code:: bash

	#!/bin/bash
	export LSST_DDS_DOMAIN=SOCS
    export NDDS_DISCOVERY_PEERS=shmem://
    
	export OPENSPLICE_LOC=${HOME}/git/ts/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux
	export OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml

	export SCHED_TOPIC_LIB=${HOME}/dds/lib
	export SCHED_CODE=${HOME}/git/ts/ts_scheduler

	export LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH}
	export PYTHONPATH=${SCHED_TOPIC_LIB}:${SCHED_CODE}:${PYTHONPATH}

	$@

The LSST_DDS_DOMAIN is important so that messages from other instances using DDS do not pollute the currently running process. It needs to be a unique name within the user's network environment.

The following instructions will refer to this wrapper script as ``drun``. 

To run the Scheduler, go to the ``gitdir/ts/ts_scheduler/ts_scheduler`` directory and run the following::

	drun python scheduler.py

The SOCS driver can be run from anywhere if the setup from the installation instructions were followed. We'll assume that you are running from ``$HOME/run_local``. To invoke a basic instance of SOCS, do the following::

	drun opsim4 -l $PWD/log -c "Running a one year sim." -v

This will run a one year simulation while passing messages between SOCS and the Scheduler via SAL/DDS. Further options are available to the driver script and can be acertained by the following::

	drun opsim -h