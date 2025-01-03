Pruebas unitarias
=================

.. important::
  Al ejecutar pruebas, deberás tener configuradas las variables de entorno necesarias en el archivo test.env. Favor de duplicar test.env-dist, cambiar su nombre a test.env y rellenar las variables necesarias.

Antes de empezar, debes configurar las siguientes variables de entorno, como mínimo:

.. code:: shell

    LIBREDTE_URL="https://libredte.cl"
    LIBREDTE_HASH="hash-libredte"
    LIBREDTE_RUT="66666666-6"

Para ejecutar las pruebas unitarias se necesita tener instaladas las dependencias del archivo requirements.txt.

Para ejecutar todas las pruebas, utilizar el siguiente comando:

.. code:: shell

    python3 tests/run.py

También es posible ejecutar un archivo de pruebas específico, indicando el archivo a utilizar. Ejemplos:

.. code:: shell

    python3 tests/run.py dte_facturacion.dte_temp.test_emitir_dte_temp
    python3 tests/run.py pagos_cobros_masivos.test_buscar_cobro_programado

Además puedes elegir una única prueba específica, utilizando la ruta completa:

.. code:: shell

    python3 tests/run.py dte_facturacion.test_emitir_dte_temp.TestEmitirDteTemp.test_emitir_dte_temp

.. important::
    Para el ejemplo anterior, se necesita tener al menos 1 DTE emitido.