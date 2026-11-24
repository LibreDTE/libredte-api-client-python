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
Pruebas de la configuración del contribuyente y del ambiente, sin red.

    python tests/run.py api_client.test_configuracion
"""

import os
import unittest
from unittest.mock import patch

from libredte.api_client import ApiClient, ApiException

HASH = '0' * 32
URL = 'https://libredte.invalid'


class TestConfiguracion(unittest.TestCase):

    """RUT del contribuyente y ambiente del SII."""

    def setUp(self) -> None:
        """Prepara un cliente con LIBREDTE_RUT definido en el entorno."""
        entorno = patch.dict(
            os.environ,
            {'LIBREDTE_RUT': '76192083-9'},
            clear=True,
        )
        entorno.start()
        self.addCleanup(entorno.stop)
        self.client = ApiClient(HASH, URL)

    def test_contribuyente_desde_el_entorno(self) -> None:
        """Sin RUT, se usa el de LIBREDTE_RUT, sin dígito verificador."""
        self.assertEqual(self.client.rut, 76192083)
        self.assertEqual(self.client.set_contribuyente(None), 76192083)

    def test_contribuyente_vacio_lo_quita(self) -> None:
        """Con '' se quita el contribuyente, aunque esté LIBREDTE_RUT."""
        self.assertIsNone(self.client.set_contribuyente(''))
        self.assertIsNone(self.client.rut)

    def test_contribuyente_invalido(self) -> None:
        """Un RUT que no es número es un error."""
        with self.assertRaises(ApiException):
            self.client.set_contribuyente('abc')

    def test_ambiente_sin_distinguir_mayusculas(self) -> None:
        """'Produccion' o ' TEST ' son válidos, como en minúsculas."""
        casos = {
            'Produccion': ApiClient.AMBIENTE_SII_PRODUCCION,
            'PALENA': ApiClient.AMBIENTE_SII_PRODUCCION,
            ' TEST ': ApiClient.AMBIENTE_SII_PRUEBAS,
            'Maullin': ApiClient.AMBIENTE_SII_PRUEBAS,
        }
        for ambiente, esperado in casos.items():
            with self.subTest(ambiente=ambiente):
                self.assertEqual(
                    self.client.set_ambiente_sii(ambiente),
                    esperado,
                )

    def test_ambiente_invalido(self) -> None:
        """Un ambiente desconocido es un error."""
        with self.assertRaises(ApiException):
            self.client.set_ambiente_sii('desarrollo')


if __name__ == '__main__':
    unittest.main(verbosity=2)
