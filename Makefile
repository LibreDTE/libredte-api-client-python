# Targets that are not files. docs, dist and tests are also folders of the
# repository: without .PHONY, make would take them as up to date.
.PHONY: all dist upload install-dev lint typecheck check tests \
	tests-readonly docs clean

# Python used to create the environment (minimum 3.14, as requires-python).
PYTHON ?= python3.14

# Named "venv" because [tool.pyright] looks for the environment there.
VENV = venv
VENV_READY = $(VENV)/.installed

all: dist

# Source distribution (sdist), built with the [build-system] of
# pyproject.toml. dist/ is emptied first, so upload sends only this build.
dist: $(VENV_READY)
	rm -rf dist
	$(VENV)/bin/python -m build --sdist

upload: dist
	$(VENV)/bin/twine upload dist/*

# Created on the first command and reinstalled when pyproject.toml changes.
# An existing environment is not created again, so its Python is kept.
$(VENV_READY): pyproject.toml
	test -x $(VENV)/bin/python || $(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -c 'import sys; sys.exit(sys.version_info < (3, 14) and "$(VENV) usa Python %s.%s; se requiere 3.14 o superior: rm -rf $(VENV)" % sys.version_info[:2])'
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -e .
	$(VENV)/bin/python -m pip install --group dev
	touch $(VENV_READY)

install-dev: $(VENV_READY)

lint: $(VENV_READY)
	$(VENV)/bin/ruff check .

typecheck: $(VENV_READY)
	$(VENV)/bin/mypy
	$(VENV)/bin/pyright

check: lint typecheck

tests: $(VENV_READY)
	$(VENV)/bin/python tests/run.py

# Subset run by the CI: the tests without network, and the ones of DTE
# temporales and cobros (they do not emit real DTE nor send emails).
tests-readonly: $(VENV_READY)
	$(VENV)/bin/python tests/run.py api_client.test_configuracion
	$(VENV)/bin/python tests/run.py api_client.test_conexion
	$(VENV)/bin/python tests/run.py api_client.test_url
	$(VENV)/bin/python tests/run.py api_client.test_manejo_errores
	$(VENV)/bin/python tests/run.py dte_facturacion.dte_temp.test_buscar_dte_temp.TestBuscarDteTemp
	$(VENV)/bin/python tests/run.py dte_facturacion.dte_temp.test_descargar_pdf_dte_temp.TestDescargarPdfDteTemp
	$(VENV)/bin/python tests/run.py dte_facturacion.dte_temp.test_descargar_xml_dte_temp.TestDescargarXmlDteTemp
	$(VENV)/bin/python tests/run.py dte_facturacion.dte_temp.test_emitir_dte_temp.TestEmitirDteTemp
	$(VENV)/bin/python tests/run.py dte_facturacion.dte_temp.test_eliminar_dte_temp.TestEliminarDteTemp
	$(VENV)/bin/python tests/run.py dte_facturacion.dte_temp.test_listar_dtes_temp.TestListarDtesTemp
	$(VENV)/bin/python tests/run.py pagos_cobros_masivos.test_buscar_cobro_programado.TestBuscarCobroProgramado
	$(VENV)/bin/python tests/run.py pagos_cobros_masivos.test_listar_cobros_masivos_programados.TestListarCobrosMasivosProgramados

# sphinx-apidoc -f regenerates the .rst of the API reference, so new modules
# are added to it.
docs: $(VENV_READY)
	$(VENV)/bin/sphinx-apidoc -f -o docs libredte
	$(VENV)/bin/sphinx-build -b html docs docs/_build/html

clean:
	rm -rf dist libredte.egg-info libredte/__pycache__ libredte/*.pyc .ruff_cache .mypy_cache
