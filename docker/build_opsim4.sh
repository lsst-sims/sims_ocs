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

PACKAGE_NAME="lsst/opsim4"
DEFAULT_DATELOC_VERSION="master"
DEFAULT_ASTROSKY_VERSION="master"
DEFAULT_OBSMOD_VERSION="master"
DEFAULT_SOCS_VERSION="master"
DEFAULT_SCHED_VERSION="master"
DEFAULT_CONFUI_VERSION="master"
NOCACHE=true

usage() {
  cat << EOD

  Usage: $(basename "$0") [options]

  This command builds an OpSim4 image.

  Available options:
    -a          Version for the Astronomical Sky Model package. Defaults to $DEFAULT_ASTROSKY_VERSION
    -d          Version for the Date/Location package. Defaults to $DEFAULT_DATELOC_VERSION
    -h          This message
    -m          Version for the Observatory Model package. Defaults to $DEFAULT_OBSMOD_VERSION
    -n          Turn off no-cache option
    -o          Version for the SOCS code. Defaults to $DEFAULT_SOCS_VERSION
    -p          Push to dockerhub after build
    -s          Version for the Scheduler code. Defaults to $DEFAULT_SCHED_VERSION
    -u          Version for the Configuration UI code. Defaults to $DEFAULT_CONFUI_VERSION

EOD
}

# get the options
while getopts hpo:s:u:d:a:m:n c; do
    case $c in
            h) usage ; exit 0 ;;
            p) PUSH=1 ;;
            o) SOCS_VERSION="$OPTARG" ;;
            s) SCHED_VERSION="$OPTARG" ;;
            u) CONFUI_VERSION="$OPTARG" ;;
            d) DATELOC_VERSION="$OPTARG" ;;
            a) ASTROSKY_VERSION="$OPTARG" ;;
            m) OBSMODEL_VERSION="$OPTARG" ;;
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
    TAG="${PACKAGE_NAME}:latest"
else
    if [[ $SOCS_VERSION =~ ^[[:digit:]] ]] ; then
        TAG="${PACKAGE_NAME}:${SOCS_VERSION}"
    else
        TAG="${PACKAGE_NAME}:branch"
    fi
fi 

if [ -z $SCHED_VERSION ] ; then
    SCHED_VERSION=$DEFAULT_SCHED_VERSION
else
    if [[ $SCHED_VERSION =~ ^[[:digit:]] ]] ; then
        SCHED_VERSION="v$SCHED_VERSION"
    fi
fi 

if [ -z $CONFUI_VERSION ] ; then
    CONFUI_VERSION=$DEFAULT_CONFUI_VERSION
fi 

if [ -z $DATELOC_VERSION ] ; then
    DATELOC_VERSION=$DEFAULT_DATELOC_VERSION
else
    DATELOC_VERSION="v$DATELOC_VERSION"
fi 

if [ -z $ASTROSKY_VERSION ] ; then
    ASTROSKY_VERSION=$DEFAULT_ASTROSKY_VERSION
else
    ASTROSKY_VERSION="v$ASTROSKY_VERSION"
fi 

if [ -z $OBSMOD_VERSION ] ; then
    OBSMOD_VERSION=$DEFAULT_OBSMOD_VERSION
else
    OBSMOD_VERSION="v$OBSMOD_VERSION"
fi 

# Build the release image

printf "Building Opsim4 image with tag: %s\n" $TAG
docker build --no-cache=${NOCACHE} \
             --build-arg SOCS_VERSION="$SOCS_VERSION" \
             --build-arg SCHED_VERSION="$SCHED_VERSION" \
             --build-arg CONFUI_VERSION="$CONFUI_VERSION" \
             --build-arg DATELOC_VERSION="$DATELOC_VERSION" \
             --build-arg ASTROSKY_VERSION="$ASTROSKY_VERSION" \
             --build-arg OBSMOD_VERSION="$OBSMOD_VERSION" \
             --tag="$TAG" opsim4

if [ $PUSH ] ; then
    printf "Pushing to Docker hub\n"
    docker push "$TAG"
fi