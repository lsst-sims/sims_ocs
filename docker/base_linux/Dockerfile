FROM centos:7.3.1611
MAINTAINER Michael Reuter <mareuter@lsst.org>

ARG GOSU_URL=https://github.com/tianon/gosu/releases/download
ARG GOSU_VERSION=1.10

RUN yum install -y \
  bzip2 \
  git \
  boost-python \
  mesa-libGL-devel \
  libXrender-devel \
  libSM-devel \
  libICE-devel \
  xorg-x11-fonts-100dpi \
  xorg-x11-fonts-Type1 \
  xorg-x11-fonts-ISO8859-1-100dpi \
  xorg-x11-fonts-misc \
  gnu-free-sans-fonts \
  liberation-*-fonts \
  dejavu-*-fonts \
  open-sans-fonts

RUN gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && curl -o /usr/local/bin/gosu -SL "${GOSU_URL}/${GOSU_VERSION}/gosu-amd64" \
    && curl -o /usr/local/bin/gosu.asc -SL "${GOSU_URL}/${GOSU_VERSION}/gosu-amd64.asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && rm -r /root/.gnupg/ \
    && chmod +x /usr/local/bin/gosu
