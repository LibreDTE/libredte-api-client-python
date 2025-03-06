all: dist

dist:
	python3 setup.py sdist

upload: dist
	twine upload dist/*

install-dev:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

tests: install-dev
	python tests/run.py

tests-dte:
	python3 tests/run.py dte_facturacion

tests-dte_real:
	python3 tests/run.py dte_facturacion.dte_real

tests-dte_rec:
	python3 tests/run.py dte_facturacion.dte_recibidos

tests-dte_temp:
	python3 tests/run.py dte_facturacion.dte_temp

tests-cobros:
	python3 tests/run.py pagos_cobros_masivos

tests-readonly:
	python3 tests/run.py dte_facturacion.dte_temp.test_buscar_dte_temp.TestBuscarDteTemp
	python3 tests/run.py dte_facturacion.dte_temp.test_descargar_pdf_dte_temp.TestDescargarPdfDteTemp
	python3 tests/run.py dte_facturacion.dte_temp.test_descargar_xml_dte_temp.TestDescargarXmlDteTemp
	python3 tests/run.py dte_facturacion.dte_temp.test_emitir_dte_temp.TestEmitirDteTemp
	python3 tests/run.py dte_facturacion.dte_temp.test_eliminar_dte_temp.TestEliminarDteTemp
	python3 tests/run.py dte_facturacion.dte_temp.test_listar_dtes_temp.TestListarDtesTemp
	python3 tests/run.py dte_facturacion.dte_real.test_emitir_dte_real.TestEmitirDteReal
	python3 tests/run.py pagos_cobros_masivos.test_buscar_cobro_programado.TestBuscarCobroProgramado
	python3 tests/run.py pagos_cobros_masivos.test_listar_cobros_masivos_programados.TestListarCobrosMasivosProgramados
	python3 tests/run.py pagos_cobros_masivos.test_pagar_cobro_dte_temp.TestPagarCobroDteTemp

docs:
	sphinx-apidoc -o docs libredte && sphinx-build -b html docs docs/_build/html

clean:
	rm -rf dist libredte.egg-info libredte/__pycache__ libredte/*.pyc
