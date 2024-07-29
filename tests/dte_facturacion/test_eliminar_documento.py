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

import unittest
from os import getenv
import json
from libredte.api_client import ApiClient, ApiException
from libredte.api_client.dte import Dte


class TestDteTemporal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        cls.receptor = getenv('TEST_RECEPTOR')
        cls.tipo_dte = getenv('TEST_DTE')
        cls.codigo_dte = getenv('TEST_CODIGO')
        cls.emisor = getenv('TEST_EMISOR')
        cls.dte = Dte()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(ApiClient.AMBIENTE_SII_PRUEBAS)
    
    def test_eliminar_dte_temporal(self):
        try:
            response = self.dte.delete_dte_temporal(self.receptor, self.tipo_dte, self.codigo_dte, self.emisor)
            dte_eliminado = response.json()

            if self.verbose:
                print('test_dte_temporal(): dte_eliminado', json.dumps(dte_eliminado))
        except ApiException as e:
            self.fail(f"ApiException: {e}")

