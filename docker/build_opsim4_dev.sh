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


# Create an OpSim4 development image
# @author Michael Reuter, LSST
# Special thanks to Brian Van Klaveren, SLAC for the nice build scripts

set -e

DEFAULT_TAG="mareuter/opsim4:opsim4-dev"

usage() {
  cat << EOD

  Usage: $(basename "$0") [options]

  This command builds an OpSim4 development image.

  Available options:
    -h          this message
    -T          Tag name. Defaults to $DEFAULT_TAG
    -p          Push to dockerhub after build

EOD
}

# get the options
while getopts hT:p c; do
    case $c in
            h) usage ; exit 0 ;;
            T) TAG="$OPTARG" ;;
            p) PUSH=1 ;;
            \?) usage ; exit 2 ;;
    esac
done

shift "$((OPTIND-1))"

if [ $# -ne 0 ] ; then
    usage
    exit 2
fi

if [ -z $TAG ]  ; then
    # Use default tag
    TAG=$DEFAULT_TAG
fi

# Build the release image

printf "Building Opsim4 development image with tag: %s\n" $TAG
docker build --no-cache=true --tag="$TAG" opsim4-dev

if [ $PUSH ] ; then
    printf "Pushing to Docker hub\n"
    docker push "$TAG"
fi