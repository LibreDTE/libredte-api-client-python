#
# LibreDTE: Cliente de API en Python.
# Copyright (C) LibreDTE <https://www.libredte.cl>
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public License (LGPL) publicada
# por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior de la misma.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN
# GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
# PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
# Public License (LGPL) para obtener una información más detallada.
#
# Debería haber recibido una copia de la GNU Lesser General Public License
# (LGPL) junto a este programa. En caso contrario, consulte
# <http://www.gnu.org/licenses/lgpl.html>.
#

"""
Ejecuta los casos de prueba de la biblioteca.

Uso: ``python tests/run.py [caso]``, por ejemplo
``python tests/run.py dte_facturacion.dte_temp``. Sin caso, ejecuta todas
las pruebas de la carpeta ``tests``.
"""

import argparse
import os
import sys
import unittest
from types import TracebackType
from typing import TYPE_CHECKING, Protocol, override

from dotenv import load_dotenv

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)


class _Flujo(Protocol):

    """Flujo de salida que ``TextTestRunner`` entrega al resultado."""

    def write(self, s: str, /) -> object:
        """Escribe el texto en el flujo."""
        ...

    def flush(self) -> object:
        """Vacía el flujo."""
        ...

    def writeln(self, arg: str | None = None, /) -> None:
        """Escribe el texto en el flujo, seguido de un salto de línea."""
        ...


# Para los chequeadores de tipos, TextTestResult es genérico en el tipo del
# flujo que recibe; en ejecución no lo es y no se puede parametrizar.
if TYPE_CHECKING:
    _ResultadoBase = unittest.TextTestResult[_Flujo]
else:
    _ResultadoBase = unittest.TextTestResult


class CustomTestResult(_ResultadoBase):

    """Resultado de las pruebas que muestra el detalle de las aserciones."""

    @override
    def addFailure(
        self,
        test: unittest.TestCase,
        err: (
            tuple[type[BaseException], BaseException, TracebackType]
            | tuple[None, None, None]
        ),
    ) -> None:
        """Muestra el detalle de una aserción fallida y registra el fallo."""
        exception_type, value, _ = err
        if exception_type is AssertionError:
            self.stream.writeln(f'\nFAIL: {test.id()}')
            self.stream.writeln(f'Assertion Error: {value}')
        # Manejo estándar para otros errores
        super().addFailure(test, err)


tests_dir = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(tests_dir, 'test.env')):
    load_dotenv(os.path.join(tests_dir, 'test.env'), override=True)

parser = argparse.ArgumentParser(
    description='Ejecución de los casos de prueba',
)
parser.add_argument(
    'test_case',
    nargs='?',
    default=None,
    help=(
        'Permite especificar un test a ejecutar '
        '(ej: "sii.test_contribuyentes")'
    ),
)
args = parser.parse_args()

loader = unittest.TestLoader()
suite = (
    loader.loadTestsFromName(args.test_case)
    if args.test_case
    else loader.discover(tests_dir)
)

runner = unittest.TextTestRunner(
    failfast=True,
    resultclass=CustomTestResult,
)
# El código de salida indica el resultado (0: todas pasan, 1: alguna falla),
# para que make y el CI fallen cuando falla una prueba.
try:
    result = runner.run(suite)
except KeyboardInterrupt:
    # Interrumpido con Ctrl+C: código estándar de SIGINT (128 + 2).
    sys.exit(130)
sys.exit(0 if result.wasSuccessful() else 1)
