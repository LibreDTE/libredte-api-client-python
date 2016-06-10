SDK de LibreDTE para Python
===========================

SDK para realizar la integración con los servicios web de LibreDTE desde Python.

Este código está liberado bajo licencia `LGPL <http://www.gnu.org/licenses/lgpl-3.0.en.html>`_.
O sea, puede ser utilizado tanto en software libre como en software privativo.

Instalación
-----------

Instalar desde PIP con:

.. code:: shell

    $ sudo pip install libredte

Desarrolladores (ayuda mental)
------------------------------

Modificar el SDK:

.. code:: shell

    $ git clone https://github.com/LibreDTE/libredte-sdk-python
    $ cd libredte-sdk-python
    $ sudo pip install -e .

Crear el paquete que se desea distribuir:

.. code:: shell

    $ sudo python setup.py sdist

Publicar el paquete a distribuir:

.. code:: shell

    $ twine upload dist/*

Más información en `<http://python-packaging-user-guide.readthedocs.io/en/latest/distributing>`_
