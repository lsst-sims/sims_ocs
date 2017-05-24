========
Usage
========

We start this section by assuming you have followed the installation instructions and are within the created Conda environment. To setup the environment for running the Operations Simulator, do::

	source stack_install_dir/loadLSST.<shell>
	source activate opsim4
	setup ts_scheduler
	setup sims_ocs

The Operations Simulator consists of running the SOCS and Scheduler. Due to the nature of the setup, a wrapper script is recommended when launching the driver script. A script has been provided `here <https://raw.githubusercontent.com/lsst-sims/opsim4_tools/master/scripts/drun>`_. The script needs to be edited to provide locations for certain variables. See the comments within the script. This script is intended for use when running multiple simulations simultaneously. 

If you wish to override your computer's hostname, the ``$OPSIM_HOSTNAME`` environmental variable can be used to achieve this.

If you only wish to run one simulation at any given time or want to connect the running simulation to another DDS stream handler, it is necessary to know the ``$OSPL_URI`` file used to execute the job. The ``drun`` script rotates this file for each use, but does provide an override mechanism when using it again. However, `this <https://raw.githubusercontent.com/lsst-sims/opsim4_tools/master/scripts/drun_static>`_ script has been provided to remove the need for knowing the ``$OSPL_URI`` file. **However**, when using this script, the simulation run must be the only one running as the DDS domain Id could conflict with another running job.

.. _running-opsim4:

Running OpSim
~~~~~~~~~~~~~

The SOCS driver can be run from anywhere if the setup from the installation instructions were followed. We'll assume that you are running from ``$HOME/run_local``. In this directory, it is recommended to have ``configs`` and ``log`` sub-directories available. This will be helpful in containing all of the various outputs when running multiple simulations. To invoke a basic instance of SOCS, do the following::

	drun opsim4 --frac-duration=1 -c "Running a one year sim." -v

This will run a one year simulation while passing messages between SOCS and the Scheduler via SAL/DDS. The SOCS driver script launches a central process for log messages coming from the SOCS and Scheduler drivers. It then launches the Scheduler driver.

Further options are available to the driver script and can be ascertained by the following::

	drun opsim4 -h
 