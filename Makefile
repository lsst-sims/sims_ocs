GH_PAGES_SOURCES = Makefile docs setup.py lsst README.rst HISTORY.rst scripts

.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 lsst tests setup.py scripts/*

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source lsst setup.py test
	coverage report -m
	coverage html
	#open htmlcov/index.html

docs:
	rm -f docs/tables/*.rst
	rm -f docs/table_descriptions.rst
	python docs/generate_tables.py
	rm -f docs/api/lsst*.rst
	rm -f docs/api/modules.rst
	sphinx-apidoc -H sims_ocs -e -o docs/api lsst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	#open docs/_build/html/index.html

gh-pages:
	git checkout gh-pages
	rm -rf api build _modules _sources _static tables
	git checkout master $(GH_PAGES_SOURCES)
	git reset HEAD
	python setup.py develop
	$(MAKE) docs
	mv -fv docs/_build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) sims_ocs.egg-info

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
