# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as _test
PACKAGE = 'sims_ocs'
MAJOR = 0
MINOR = 2
PATCH = 0
VERSION = "{0}.{1}.{2}".format(MAJOR, MINOR, PATCH)

MODULE = "lsst.sims.ocs"

class quiet_test(_test):
    def finalize_options(self):
        self.verbose = False
        _test.finalize_options(self)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

def write_version(filename="version.py"):
    parts = MODULE.split('.')
    parts.append(filename)
    with open(os.path.join(*parts), 'w') as vfile:
        vfile.write("__version__ = '{0}'".format(VERSION) + os.linesep)
        vfile.write("__version_info__ = ({0}, {1}, {2})".format(MAJOR, MINOR, PATCH) + os.linesep)
        vfile.write(os.linesep)
        vfile.write("__all__ = ('__version__', '__version_info__')" + os.linesep)

if __name__ == "__main__":
    write_version()

    setup(
        name=PACKAGE,
        version=VERSION,
        description="Package that simulates the OCS to drive the Scheduler",
        long_description=readme + os.linesep * 2 + history,
        author="Michael Reuter",
        author_email='mareuter@lsst.org',
        url='https://github.com/lsst-sims/sims_ocs',
        cmdclass={
            'test': quiet_test,
        },
        scripts=['scripts/opsim4'],
        packages=[
            'lsst',
        ],
        package_dir={'lsst':
                     'lsst'},
        include_package_data=True,
        install_requires=requirements,
        license="GPL",
        zip_safe=False,
        keywords=PACKAGE,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research'
            'Topic :: Scientific/Engineering :: Astronomy'
            'License :: OSI Approved :: GPL License',
            'Natural Language :: English',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],
        test_suite='tests',
        tests_require=test_requirements
    )
