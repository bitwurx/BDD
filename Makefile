all: install

install:
	python setup.py install

clean:
	rm -rf build dist bdist sdist BDD.egg-info

