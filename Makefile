all: dist

dist:
	python3 setup.py sdist

upload: dist
	twine upload dist/*

install-dev:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

tests: install-dev
	python tests/run.py

tests_dte:
	python3 tests/run.py dte_facturacion

tests_dte_real:
	python3 tests/run.py dte_facturacion.dte_real

tests_dte_rec:
	python3 tests/run.py dte_facturacion.dte_recibidos

tests_dte_temp:
	python3 tests/run.py dte_facturacion.dte_temp

tests_cobros:
	python3 tests/run.py pagos_cobros_masivos

docs:
	sphinx-apidoc -o docs libredte && sphinx-build -b html docs docs/_build/html

clean:
	rm -rf dist libredte.egg-info libredte/__pycache__ libredte/*.pyc
