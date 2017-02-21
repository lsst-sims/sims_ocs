============
Installation
============

.. warning::

	The current installation requires multiple repositories and a mixture of environments. It also only works on a Linux operating system. It has been tested only CentOS 7.

.. note::

	If performing the installation on a virtual machine, it needs the following minimum requirements:

		* Memory: 10 GB (minimum)
		* Number of processors: 3 (4 recommended)
		* Network: Bridged adapter

General Installation Notes
--------------------------

Due to the heavy use of repositories for this installation, the instructions will assume you have created a ``git`` directory in your ``$HOME`` directory. This will be referenced as ``gitdir``. The individual repository installation instructions will give further advice on directory names. This is intended to make the usage "easier". Also, all instructions are based around using the code, not developing it.

SAL Installation
----------------

The SAL (Software Abstraction Layer) is a wrapper around the DDS (Data Distribution Service) layer and provides binding to Python. This requires the OpenSplice and SAL repositories from Telescope and Site. Inside the ``gitdir`` create a directory called ``ts``. Go into this directory and run the following::

	git clone https://github.com/lsst-ts/ts_opensplice.git
	git clone https://github.com/lsst-ts/ts_sal.git

In the SAL clone, there is a user guide that documents installation and setup of SAL. Its location is ``gitdir/ts/ts_sal/SAL_User_Guide.pdf``. Follow section 1 and the main part of section 2. Sub-sections (those colored blue) 2.1 and 2.2 are redundant as we've already installed the SAL. Sub-section 2.3 is replaced by the following documentation that is specific to this SOCS/Scheduler setup.

Build Scheduler Topic Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``$HOME/dds`` directory and copy the ``gitdir/ts/ts_sal/setup.env`` to it. Also, create a ``$HOME/dds/lib`` directory for later. The following variables need to be edited in ``setup.env`` to reflect your setup::

	export LSST_SDK_INSTALL=$HOME/git/ts/ts_sal
	export OSPL_HOME=$HOME/git/ts/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux

All other variables can remain the same. Once the edits are complete, do::

	source $HOME/dds/setup.env

The configuration should complete without errors. Go back to ``gitdir/ts/ts_sal`` and do the following::

	git checkout -t origin/feature/scheduler_xml_devel
	cd test
	salgenerator scheduler validate
	salgenerator scheduler sal cpp
	salgenerator scheduler sal python

Once the build is complete, the topic and supporting library need to be copied via the following::

	cp scheduler/cpp/src/SALPY_scheduler.so $HOME/dds/lib
	cp scheduler/cpp/libsacpp_scheduler_types.so $HOME/dds/lib

Scheduler and SOCS Source Code
------------------------------

There is a prerequisite repository for the system that needs to be downloaded. Create a ``gitdir/lsst`` directory, go into that and run::

	git clone https://github.com/lsst/sims_skybrightness_pre.git

The Scheduler repository should also be cloned to ``gitdir/ts`` via the following::

	git clone https://github.com/lsst-ts/ts_scheduler.git

The SOCS repository should be cloned into the ``gitdir``. Create a directory there called ``lsst-sims``, go into that and run the following::

	git clone https://github.com/lsst-sims/sims_ocs.git

LSST Stack Installation
~~~~~~~~~~~~~~~~~~~~~~~

The SOCS and Scheduler installation require a set of packages from Python and the LSST Science Pipelines. 
Follow the installation instructions from `here <https://pipelines.lsst.io/install/newinstall.html#installing-from-source-with-newinstall-sh>`_ to get a minimal setup. Go ahead and let the stack software provide Python unless you feel comfortable providing your own. Follow the instructions to get into the stack environment. The instructions will refere to the stack installation directory as ``stack_install_dir``. It is recommended to use a conda environment especially if you are going to use the stack for other reasons. To create an environment, do the following::

    conda create -n opsim4 --clone=root
    source activate opsim4
    conda remove conda-env

The last line is necessary since the create complains about that package being duplicated. Next, install the following stack packages::

    eups distrib install sims_utils -t sims
    eups distrib install pex_config -t sims

Once this is complete, perform the following operation::

    conda update sqlalchemy

If one wishes to develop the code, being able to run the unit tests, check style compliance and generate the documentation is a must. To do this, these packages need to be installed::

	conda install mock sphinx sphinx_rtd_theme flake8 coverage pytest

There is one package that is required for the documentation but is not available via the conda packaging system. To get this package, do::

	pip install rst

With the environment setup, we need to declare and setup the prerequisite repos and then SOCS and Scheduler packages so they can be used. 

Declare the pre-calculated sky brightness model::

	cd gitdir/lsst/sims_skybrightness_pre
	eups declare sims_skybrightness_pre git -r . -c
	setup sims_skybrightness_pre git
	scons

Declare the Scheduler::

	cd gitdir/ts/ts_scheduler
	eups declare ts_scheduler git -r . -c
	setup ts_scheduler
	scons

To declare and setup SOCS, do::

	cd gitdir/lsst-sims/sims_ocs
	eups declare sims_ocs git -r . -c
	setup sims_ocs
	scons

**NOTE**: The declaration steps only need to be done once. After that, when returning to the same conda environment, do::

	source stack_install_dir/loadLSST.<shell>
	source activate opsim4
	setup sims_ocs

Sky Brightness Model Data
-------------------------

In the previous section, the pre-calculated sky brightness model was installed, but it does not come with the data required to run. The required data is ~65 GB in size, so create a directory for it. The instructions will assume one was created as ``$HOME/sky_brightness_data``. After running the ``setup sims_ocs`` command, change to this directory and execute the following::

	$SIMS_SKYBRIGHTNESS_PRE_DIR/data/data_down.sh -o 

While this instruction is executing, the instructions may continue to be followed, but OpSim will not function correctly until the data is done downloading.

.. _installation-database:

Database Setup
--------------

SOCS provides a SQLite interface for simulation information storage. A script, ``manage_db`` has been created to help setup the necessary simulation related items. To see the options available::

	manage_db -h

The following assumes a ``$HOME/run_local`` directory with an ``output`` sub-directory already available. To create the SQLite setup, run the following::

	manage_db --save-dir=$HOME/run_local/output

This process creates in ``$HOME/run_local/output`` a ``<hostname>_session.db`` file where ``<hostname>`` is the name of your computer. If you have a DNS provided hostname and would like to have a more "normal" name, add the ``$OPSIM_HOSTNAME`` environmental variable to the session before running the above command. The script also creates a configuration file in ``$HOME/.config`` called ``opsim4`` and it contains the database setup information. This will allow you to not have to provide that information to the main simulation driver script.

If you wish to clear out your database and start over, but begin at the next run number from 
where you left off, this task can be accomplished. The ``-s`` flag to the ``manage_db`` will adjust the starting point for the run numbers. You will need the last run number generated and then pass that number incremented by one to the flag. The run number is written into the configuration file for later use when running the simulation.
