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

También es posible ejecutar un archivo de pruebas específico, indicando el archivo a utilizar. Ejemplo:

.. code:: shell

    python3 tests/run.py dte_facturacion.test_generar_dte_temporal

Además puedes elegir una única prueba específica, utilizando la ruta completa:

.. code:: shell

    python3 tests/run.py dte_facturacion.test_buscar_documento_emitido.TestBuscarDocumentoEmitido.test_dte_buscar_documento_emitido

.. important::
    Para el ejemplo anterior, se necesita tener al menos 1 DTE emitido.