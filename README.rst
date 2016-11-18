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

LXML en Microsoft Windows
~~~~~~~~~~~~~~~~~~~~~~~~~

En algunas versiones de Microsoft Windows (al menos 8 y 10) la instalación con
PIP falla debido a que no es posible instalar LXML. Para solucionar esto y poder
instalar el SDK es necesario instalar LXML de manera manual. Se puede descargar
`una versión binaria de LXML <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`_
según la versión de Python que estemos usando.

Supongamos que tenemos Python 3.5 de 32 bits (independientemente que el sistema
operativo sea de 64 bits). Debemos descargar el siguiente archivo
`lxml‑3.6.4‑cp35‑cp35m‑win32.whl <http://www.lfd.uci.edu/~gohlke/pythonlibs/g7ckv9dk/lxml-3.6.4-cp35-cp35m-win32.whl>`_
y procedemos a instalar con

.. code:: shell

    > pip.exe install lxml-3.6.4-cp35-cp35m-win32.whl

Si usas otra versión de Python descarga la LXML que corresponda.

Cuando tengas instalada la LXML procede a instalar el SDK de LibreDTE con PIP.

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
