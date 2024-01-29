LibreDTE: Cliente de API en Python
==================================

.. image:: https://badge.fury.io/py/libredte.svg
    :target: https://pypi.org/project/libredte
.. image:: https://img.shields.io/pypi/status/libredte.svg
    :target: https://pypi.org/project/libredte
.. image:: https://img.shields.io/pypi/pyversions/libredte.svg
    :target: https://pypi.org/project/libredte
.. image:: https://img.shields.io/pypi/l/libredte.svg
    :target: https://raw.githubusercontent.com/LibreDTE/libredte-api-client-python/master/COPYING

Cliente para realizar la integración con los servicios web de `LibreDTE <https://www.libredte.cl>`_ desde Python.

Instalación y actualización
---------------------------

Instalar usando un entorno virtual y PIP con:

.. code:: shell

    python3 -m venv venv
    source venv/bin/activate
    pip install libredte

Actualizar usando PIP con:

.. code:: shell

    pip install libredte --upgrade

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

Licencia
--------

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
`GNU Lesser General Public License <http://www.gnu.org/licenses/lgpl.html>`_.

Enlaces
-------

- `Sitio web LibreDTE <https://www.libredte.cl>`_.
- `Código fuente en GitHub <https://github.com/libredte/libredte-api-client-python>`_.
- `Paquete en PyPI <https://pypi.org/project/libredte>`_.
- `Documentación en Read the Docs <https://libredte.readthedocs.io/es/latest>`_.
