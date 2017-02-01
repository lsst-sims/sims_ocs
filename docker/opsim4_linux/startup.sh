#!/bin/bash
whoami
groupadd -g ${GID} ${USER}
useradd -m -u ${UID} -g ${GID} ${USER}
chown -R ${USER}:${USER} /lsst
chown ${USER}:${USER} /opsim
chown ${USER}:${USER} /home/opsim

export LSST_DDS_DOMAIN=SOCS-DOCKER-${HOSTNAME}
gosu ${USER} /bin/bash
#/bin/bash