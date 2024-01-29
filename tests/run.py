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

import argparse
from dotenv import load_dotenv
import os
import sys
import unittest

# Modificar directorio para incluir el repositorio al PATH de Python y se
# encuentre el módulo de libredte sin tener que instalarlo
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)

# Clase especial para resultado de los tests
class CustomTestResult(unittest.TextTestResult):
    def addFailure(self, test, err):
        exception_type, value, traceback = err
        if exception_type is AssertionError:
            self.stream.writeln(f"\nFAIL: {test.id()}")
            self.stream.writeln(f"Assertion Error: {value}")
        else:
            # Manejo estándar para otros errores
            super().addFailure(test, err)

# Directorio de tests
tests_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar variables de entorno para los tests
if not load_dotenv(os.path.join(tests_dir, 'test.env'), override=True):
    print("\n[Error] No fue posible cargar las variables de entorno para los tests.")
    print(f"Corroborar que exista el archivo {tests_dir}/test.env y posea las variables definidas.\n")
    sys.exit()

# Determinar si se pidió un test específico o se ejecutan todos
parser = argparse.ArgumentParser(description='Ejecución de los casos de prueba')
parser.add_argument(
    'test_case',
    nargs = '?',
    default = None,
    help = 'Permite especificar un test a ejecutar (ej: "sii.test_contribuyentes")'
)
args = parser.parse_args()

# Cargar el test solicitado o todos los del directorio de tests
loader = unittest.TestLoader()
suite = loader.loadTestsFromName(args.test_case) if args.test_case else loader.discover(tests_dir)

# Ejecutar los tests
runner = unittest.TextTestRunner(failfast=True, resultclass=CustomTestResult)
try:
    runner.run(suite)
except KeyboardInterrupt:
    pass
