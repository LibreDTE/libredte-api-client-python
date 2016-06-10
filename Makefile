all: install dist

install:
	sudo pip install -e .

dist:
	sudo python setup.py sdist

upload: dist
	twine upload dist/*

clean:
	sudo rm -rf dist libredte.egg-info libredte/__pycache__ libredte/*.pyc ejemplos/*.pdf
