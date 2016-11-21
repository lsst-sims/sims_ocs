#!/bin/bash
export LSST_DDS_DOMAIN=SOCS-DOCKER
export NDDS_DISCOVERY_PEERS=builtin.shmem://
export OPENSPLICE_LOC=${HOME}/repos/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux
export OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml
export SCHED_TOPIC_LIB=${HOME}/dds/lib
export LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH}
export PYTHONPATH=${SCHED_TOPIC_LIB}:${PYTHONPATH}
export PATH=$HOME/miniconda/bin:$PATH

source eups-setups.sh
setup sims_ocs

/bin/bash