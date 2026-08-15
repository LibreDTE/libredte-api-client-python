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

from tests.dte_facturacion.abstract_dte_facturacion import AbstractDteFacturacion
from libredte.api_client import ApiException

from os import getenv

import json

class TestListarDtesReales(AbstractDteFacturacion):
    """
    Clase de pruebas para listar DTEs reales.
    """

    @classmethod
    def setUpClass(cls):
        """
        Método de inicialización de variables y clases a utilizar.
        """
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(cls.dte.client.AMBIENTE_SII_PRUEBAS)

    def test_listar_dtes_reales(self):
        """
        Método de test para obtener una lista de DTEs reales.

        IMPORTANTE: Se necesita una firma electrónica para emitir DTEs
        reales, y por lo tanto listarlos.
        """
        try:
            # Se llama al método del abstract para listar DTEs reales.
            response = self._listar_dtes_reales(self.contribuyente_rut)

            # Si el listado no falla, el programa pasa automáticamente.
            self.assertTrue(True)

            # Si verbose es True, se despliega en pantalla el resultado.
            if self.verbose:
                print(
                    'test_listar_dte_reales() dtes_reales:',
                    json.dumps(response.json())
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception.
            self.fail('ApiException: %(e)s' % {'e' : e})