FROM lsst/opsim4:opsim4-latest
MAINTAINER Michael Reuter <mareuter@lsst.org>

USER root
# Add building packages
RUN yum install -y make

USER opsim

# Add Conda building requirements
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    conda install -y coverage flake8 mock pytest sphinx sphinx_rtd_theme && \
    pip install rst && rm -rf miniconda/pkgs"
