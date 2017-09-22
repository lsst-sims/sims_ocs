========
Usage
========

We start this section by assuming you have followed the installation instructions and are within the created Conda environment. To setup the environment for running the Operations Simulator, do::

	source stack_install_dir/loadLSST.<shell>
	source activate opsim4
	setup ts_scheduler
	setup sims_ocs

The Operations Simulator consists of running the SOCS and Scheduler along with a central logging process. Due to the nature of the setup, a wrapper script is recommended when launching the driver script. Two scripts have been provided in the ``opsim4_tools`` LSST Simulations organization GitHub repository. Both scripts need to be edited to provide locations for certain variables. See the comments within each script.

The `first <https://raw.githubusercontent.com/lsst-sims/opsim4_tools/master/scripts/drun>`_ script, called ``drun``, is intended for use when running multiple simulations simultaneously. In order to keep the DDS messages from each simulation from potentially killing another running simulation, the ``drun`` script creates a dynamic, local DDS configuration file in the execution directory. The configuration file, called ``.osplN.xml`` where ``N`` is an integer, contains the dynamically allocated DDS domain Id which is represented by the ``N``. One of these files will be generated for each invocation of ``drun``. The ``drun`` script increments ``N`` on each invocation by looking at the ``.osplN.xml`` files already present in the execution directory. Under normal circumstances the dynamic configuration file is removed upon completion of ``drun``. An exception to this is forceably killing a job via ``ctrl+c`` or ``kill``. In this case, the dynamic configuration file cleanup does not occur and must be completed manually. If the cleanup does not occur, the operator runs the risk of making subsequent jobs access port numbers that are not specified in the firewall rules. Port range setup for multiple jobs was discussed in the :ref:`SAL installation<installation-sal_installation>` instructions and is tied to a given number of jobs for a machine. If the domain Id goes over the number of jobs minus 1, all DDS traffic is blocked for that simulation and message receiving loops will timeout causing the simulation to not work properly. The DDS configuration file that is associated with a given simulation can be found near the top of the corresponding log file and finding the ``$OSPL_URI`` entry. This is important to know if you want to attach a listener process, like a live viewer, to the running simulation or to clean up a killed job without effecting other running jobs.

The `second <https://raw.githubusercontent.com/lsst-sims/opsim4_tools/master/scripts/drun_static>`_ script, called ``drun_static``, is intended for only running one simulation at any given time. This script points to a DDS configuration file that always has the same domain Id. **HOWEVER**, when using this script, the simulation run must be the only simulation running as the DDS domain Id will conflict with another running simulation. ``drun_static`` can be used to attach a listener process to the running simulation without any issues.

.. _running-opsim4:

Running OpSim
~~~~~~~~~~~~~

The SOCS driver can be run from anywhere if the setup from the installation instructions were followed. We'll assume that you are running from ``$HOME/run_local``. In this directory, it is recommended to have ``configs`` and ``log`` sub-directories available. This will be helpful in containing all of the various outputs when running multiple simulations. To invoke a basic instance of SOCS, do the following::

	drun opsim4 --frac-duration=1 -c "Running a one year sim." -v

This will run a one year simulation while passing messages between SOCS and the Scheduler via SAL/DDS. The SOCS driver script launches a central process for log messages coming from the SOCS and Scheduler drivers. It then launches the Scheduler driver.

Further options are available to the driver script and can be ascertained by the following::

	drun opsim4 -h
 
Saving Configuration
--------------------

The full configuration used for a particular simulation can be saved after the execution of the simulation. This is accomplished by using ``--save-config`` flag::

	drun opsim4 --frac-duration=0.003 -c "Testing config saving" --save-config

This will cause the creation of a ``config_<session Id>`` directory. More concretely, if the session Id for the above execution was 2100, this will result in a directory called ``config_2100`` being created in the execution directory. Inside ``config_2100`` will be a Python file for each of the configuration classes contained within the SOCS code base. The values in those files will reflect any override values passed in at the beginning of the simulation.

If the configuration saving flag is used regularly, many directories could accumulate in the execution directory. Another directory can be used to organize the numerous ``config_<session Id>`` directories. This is accomplished by using the ``--config-save-path`` flag::

	drun opsim4 --frac-duration=0.003 -c "Testing config saving" --save-config --config-save-path=$PWD/configs

With this flag, the created ``config_<session Id>`` directory will be under ``$PWD/configs``. If any part of the path does not exist, it will be created before the save is executed.
