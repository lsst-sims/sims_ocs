========
Usage
========

We start this section by assuming you have followed the installation instructions and are within the created Conda environment. To setup the environment for running the Operations Simulator, do::

	source stack_install_dir/loadLSST.<shell>
	setup sims_ocs

The Operations Simulator consists of running the SOCS and Scheduler. Due to the nature of the setup, a wrapper script is recommended when launching the driver script. If you have followed the installation recommendations, a highly recommended example is below.

.. code:: bash

	#!/bin/bash
	set -e

	while getopts t: c; do
	    case $c in
	            t) TAG="$OPTARG" ;;
	            \?) exit 1 ;;
	    esac
	done

	shift "$((OPTIND-1))"

	if [ -z $TAG ] ; then 
	    extra_tag=$(date +%s)
	else
	    extra_tag=${TAG}
	fi
	echo ${extra_tag}

	export LSST_DDS_DOMAIN=MyDomain_${extra_tag}
	export NDDS_DISCOVERY_PEERS=builtin.shmem://

	export OPENSPLICE_LOC=${HOME}/git/ts/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux
	export OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml

	export SCHED_TOPIC_LIB=${HOME}/dds/lib

	export LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH}
	export PYTHONPATH=${SCHED_TOPIC_LIB}:${PYTHONPATH}

	export SIMS_SKYBRIGHTNESS_DATA=${HOME}/sky_brightness_data

	$@

The ``LSST_DDS_DOMAIN`` is important so that messages from other instances using DDS do not pollute the currently running process. It needs to be a unique name within the user's network environment. The following instructions will refer to this wrapper script as ``drun``. 

The ``SIMS_SKYBRIGHTNESS_DATA`` is needed to tell the sky brightness model code where its data is stored. 

.. _running-opsim4:

Running OpSim
~~~~~~~~~~~~~

The SOCS driver can be run from anywhere if the setup from the installation instructions were followed. We'll assume that you are running from ``$HOME/run_local``. In this directory, it is recommended to have ``configs`` and ``log`` sub-directories available. This will be helpful in containing all of the various outputs when running multiple simulations. To invoke a basic instance of SOCS, do the following::

	drun opsim4 -c "Running a one year sim." -v

This will run a one year simulation while passing messages between SOCS and the Scheduler via SAL/DDS. The SOCS driver script launches a central process for log messages coming from the SOCS and Scheduler drivers. It then launches the Scheduler driver.

Further options are available to the driver script and can be ascertained by the following::

	drun opsim4 -h
 