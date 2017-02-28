SDK de LibreDTE para Python
===========================

.. image:: https://badge.fury.io/py/libredte.svg
    :target: https://pypi.python.org/pypi/libredte
.. .. image:: https://img.shields.io/pypi/status/libredte.svg
    :target: https://pypi.python.org/pypi/libredte
.. .. image:: https://img.shields.io/pypi/pyversions/libredte.svg
    :target: https://pypi.python.org/pypi/libredte
.. .. image:: https://img.shields.io/pypi/l/libredte.svg
    :target: https://raw.githubusercontent.com/LibreDTE/libredte-lib/master/COPYING

SDK para realizar la integración con los servicios web de LibreDTE desde Python.

Términos y condiciones de uso
-----------------------------

Al utilizar este proyecto, total o parcialmente, automáticamente se acepta
cumplir con los `términos y condiciones de uso <https://wiki.libredte.cl/doku.php/terminos>`_
que rigen a LibreDTE. La `Licencia Pública General Affero de GNU (AGPL) <https://raw.githubusercontent.com/LibreDTE/libredte-lib/master/COPYING>`_
sólo aplica para quienes respeten los términos y condiciones de uso. No existe
una licencia comercial de LibreDTE, por lo cual no es posible usar el proyecto
si no aceptas cumplir dichos términos y condiciones.

La versión resumida de los términos y condiciones de uso de LibreDTE que
permiten utilizar el proyecto, son los siguientes:

- Tienes la libertad de: usar, estudiar, distribuir y cambiar LibreDTE.
- Si utilizas LibreDTE en tu software, el código fuente de dicho software deberá
  ser liberado de manera pública bajo licencia AGPL.
- Si haces cambios a LibreDTE deberás liberar de manera pública el código fuente
  de dichos cambios bajo licencia AGPL.
- Debes hacer referencia de manera pública en tu software al proyecto y autor
  original de LibreDTE, tanto si usas LibreDTE sin modificar o realizando
  cambios al código.

Es obligación de quienes quieran usar el proyecto leer y aceptar por completo
los `términos y condiciones de uso <https://wiki.libredte.cl/doku.php/terminos>`_.

Si quieres una versión `LGPL <http://www.gnu.org/licenses/lgpl-3.0.en.html>`_
de este código, anterior pero funcional, revisa en
`LibreDTE SDK Python v1.0.0a9 (LGPL) <https://github.com/LibreDTE/libredte-sdk-python/releases/tag/v1.0.0a9>`_.
Sólo esa versión puede ser usada en código privativo, la actual no.

Instalación
-----------

Instalar desde PIP con:

.. code:: shell

    $ sudo pip install libredte

Si estás en Microsoft Windows, debes instalar además
`pypiwin32 <https://pypi.python.org/pypi/pypiwin32>`_.

Actualización
-------------

Actualizar desde PIP con:

.. code:: shell

    $ sudo pip install libredte --upgrade

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
