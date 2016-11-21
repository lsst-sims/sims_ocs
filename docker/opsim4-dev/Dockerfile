FROM mareuter/opsim4:opsim4
MAINTAINER Michael Reuter <mareuter@lsst.org>

# Add Conda development requirements
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    conda install -y coverage flake8 mock pytest sphinx sphinx_rtd_theme && \
    pip install rst"
