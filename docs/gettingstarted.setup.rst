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
