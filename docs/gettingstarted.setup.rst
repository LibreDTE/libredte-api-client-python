Configuración
=============

Autenticación en LibreDTE
-------------------------

Lo más simple, y recomendado, es usar una variable de entorno con el
`hash del usuario <https://libredte.cl/usuarios/perfil#datos:hashField>`_,
la cual será reconocida automáticamente por el cliente:

.. code:: shell

    export LIBREDTE_HASH="aquí-tu-hash-de-usuario"

Si no se desea usar una variable de entorno, al instanciar los objetos se
deberá indicar el hash del usuario. Ejemplo:

.. code:: python

    import libredte
    LIBREDTE_HASH="aquí-tu-hash-de-usuario"
    client = libredte.api_client.ApiClient(LIBREDTE_HASH)

Si utilizas LibreDTE Edición Comunidad deberás además configurar la URL
de tu servidor. Ejemplo:

.. code:: shell

    export LIBREDTE_URL="https://libredte.example.com"

Y si deseas hacerlo sin la variable de entorno, debes pasar la URL como
segundo parámetro en el constructor del cliente:

.. code:: python

    import libredte
    LIBREDTE_HASH="aquí-tu-hash-de-usuario"
    LIBREDTE_URL="https://libredte.example.com"
    client = libredte.api_client.ApiClient(LIBREDTE_HASH, LIBREDTE_URL)

.. note::
  La URL debe usar HTTPS: con ``http://`` el hash del usuario viaja sin
  cifrar, y el cliente emite un aviso (excepto para ``localhost``). Si el
  servidor responde con una redirección (por ejemplo, de ``http://`` a
  ``https://``), el cliente no la sigue y lanza ``ApiException`` indicando
  la URL a la que redirige: configure esa URL.

Contribuyente y ambiente del SII
--------------------------------

El cliente también reconoce automáticamente el RUT del contribuyente con el
que se opera y el ambiente del SII (producción o pruebas), que se envían en
cada solicitud a la API:

.. code:: shell

    export LIBREDTE_RUT="76192083-9"
    export LIBREDTE_AMBIENTE="pruebas"

El RUT se puede indicar con o sin dígito verificador. Los valores válidos para
el ambiente son ``0``, ``produccion``, ``prod`` o ``palena`` para producción, y
``1``, ``pruebas``, ``test`` o ``maullin`` para pruebas, sin distinguir
mayúsculas.

También se pueden configurar sin variables de entorno, con los métodos del
cliente:

.. code:: python

    client.set_contribuyente('76192083-9')
    client.set_ambiente_sii(client.AMBIENTE_SII_PRUEBAS)

Tiempo de espera
----------------

Las solicitudes esperan como máximo 10 segundos para conectar y 300
segundos para recibir la respuesta. Se puede cambiar al crear el cliente,
o con ``api_timeout`` en las clases de la API (``Dte``, ``Cobros``, etc.):

.. code:: python

    from libredte.api_client.dte import Dte
    dte = Dte(api_timeout=(5, 60))  # 5 s para conectar, 60 s de respuesta
    dte = Dte(api_timeout=None)     # sin límite de espera

Si se supera el tiempo, se lanza ``ApiException`` con el mensaje
"Error de timeout".

Si no logra conectarse al servidor, el cliente reintenta hasta 3 veces
(esperando 0, 1 y 2 segundos). Una solicitud que llegó al servidor no se
reintenta, ya que operaciones como emitir un DTE no se deben repetir.
