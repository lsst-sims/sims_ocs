#!/bin/bash
export LSST_DDS_DOMAIN=SOCS-DOCKER-${HOSTNAME}
/bin/bash --rcfile /home/opsim/.opsim4_profile
