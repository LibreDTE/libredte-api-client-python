Pruebas unitarias
=================

.. important::
  Al ejecutar pruebas, deberás tener configuradas las variables de entorno necesarias en el archivo test.env. Favor de duplicar test.env-dist, cambiar su nombre a test.env y rellenar las variables necesarias.

Antes de empezar, debes configurar las siguientes variables de entorno, como mínimo:

.. code:: shell

    LIBREDTE_URL="https://libredte.cl"
    LIBREDTE_HASH="hash-libredte"
    LIBREDTE_RUT="66666666-6"

Para ejecutar las pruebas unitarias se necesita el entorno de desarrollo, con
Python 3.14 o superior, la biblioteca y las dependencias de desarrollo
(grupo ``dev`` de ``pyproject.toml``). El entorno se crea en la carpeta
``venv`` con:

.. code:: shell

    make install-dev

Para ejecutar todas las pruebas, utilizar el siguiente comando:

.. code:: shell

    make tests

.. warning::
    Las pruebas usan la API real con el contribuyente configurado: emiten
    DTE temporales y reales (en el ambiente de pruebas del SII), pagan cobros
    y envían correos. Los DTE temporales que emiten se eliminan al terminar
    cada prueba. Para ejecutar solo el conjunto que usa el CI, que no emite
    DTE reales, ni paga cobros, ni envía correos, utilizar
    ``make tests-readonly``.

O, con el entorno activado (``source venv/bin/activate``):

.. code:: shell

    python3 tests/run.py

También es posible ejecutar un archivo de pruebas específico, indicando el archivo a utilizar. Ejemplos:

.. code:: shell

    python3 tests/run.py dte_facturacion.dte_temp.test_emitir_dte_temp
    python3 tests/run.py pagos_cobros_masivos.test_buscar_cobro_programado

Además puedes elegir una única prueba específica, utilizando la ruta completa:

.. code:: shell

    python3 tests/run.py dte_facturacion.dte_temp.test_emitir_dte_temp.TestEmitirDteTemp.test_emitir_dte_temp

.. important::
    Las pruebas de ``dte_facturacion.dte_real`` usan el DTE emitido más
    reciente de los últimos 30 días, y las de
    ``dte_facturacion.dte_recibidos`` el DTE recibido más reciente. Si no hay,
    esas pruebas se saltan (aparecen como *skipped*). Las que envían correos
    se saltan si no está configurada la variable de entorno ``TEST_EMAIL``.

Las pruebas de ``api_client`` no usan la API real ni requieren las variables
de entorno: simulan las respuestas de la API o usan un servidor local:

.. code:: shell

    python3 tests/run.py api_client.test_configuracion
    python3 tests/run.py api_client.test_conexion
    python3 tests/run.py api_client.test_manejo_errores
    python3 tests/run.py api_client.test_url

Revisión de código
------------------

Antes de enviar cambios, el código debe pasar el linter (Ruff) y los
chequeos de tipos en modo estricto (MyPy y Pyright):

.. code:: shell

    make check