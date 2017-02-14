#!/bin/sh

# LSST Simulations
# Copyright 2016 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.


# Create an OpSim4 image
# @author Michael Reuter, LSST
# Special thanks to Brian Van Klaveren, SLAC for the nice build scripts

set -e

PACKAGE_NAME="lsst/opsim4:linux"
DEFAULT_SOCS_VERSION="master"
DEFAULT_SCHED_VERSION="master"
DEFAULT_CONFUI_VERSION="master"
DEFAULT_SIMS_VERSION="2.3.1"
NOCACHE=true

usage() {
  cat << EOD

  Usage: $(basename "$0") [options]

  This command builds an OpSim4 image.

  Available options:
    -h          this message
    -p          Push to dockerhub after build
    -s          Version number for SIMS Conda channel. Defaults to $DEFAULT_SIMS_VERSION
    -o          Version for the SOCS code. Defaults to $DEFAULT_SOCS_VERSION
    -d          Version for the Scheduler code. Defaults to $DEFAULT_SCHED_VERSION
    -u          Version for the Configuration UI code. Defaults to $DEFAULT_CONFUI_VERSION
    -n          Turn off no-cache option.

EOD
}

# get the options
while getopts hps:o:d:u:n c; do
    case $c in
            h) usage ; exit 0 ;;
            p) PUSH=1 ;;
            s) SIMS_VERSION="$OPTARG" ;;
            o) SOCS_VERSION="$OPTARG" ;;
            d) SCHED_VERSION="$OPTARG" ;;
            u) CONFUI_VERSION="$OPTARG" ;;
			n) NOCACHE=false ;;
            \?) usage ; exit 2 ;;
    esac
done

shift "$((OPTIND-1))"
if [ $# -ne 0 ] ; then
    usage
    exit 2
fi

if [ -z $SOCS_VERSION ] ; then
    SOCS_VERSION=$DEFAULT_SOCS_VERSION
    TAG="${PACKAGE_NAME}-latest"
else
    TAG="${PACKAGE_NAME}-${SOCS_VERSION}"
fi

if [ -z $SIMS_VERSION ] ; then
    SIMS_VERSION=$DEFAULT_SIMS_VERSION
fi 

if [ -z $SCHED_VERSION ] ; then
    SCHED_VERSION=$DEFAULT_SCHED_VERSION
else
    SCHED_VERSION="v$SCHED_VERSION"
fi 

if [ -z $CONFUI_VERSION ] ; then
    CONFUI_VERSION=$DEFAULT_CONFUI_VERSION
fi 

# Build the release image

printf "Building Opsim4 image with tag: %s\n" $TAG
docker build --no-cache=${NOCACHE} \
			 --tag="$TAG" opsim4_linux
#             --build-arg SIMS_VERSION="$SIMS_VERSION" \
#             --build-arg SOCS_VERSION="$SOCS_VERSION" \
#             --build-arg SCHED_VERSION="$SCHED_VERSION" \
#             --build-arg CONFUI_VERSION="$CONFUI_VERSION" \
             
if [ $PUSH ] ; then
    printf "Pushing to Docker hub\n"
    docker push "$TAG"
fi