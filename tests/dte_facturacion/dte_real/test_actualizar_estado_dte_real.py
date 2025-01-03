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
from libredte.api_client import ApiClient, ApiException

from os import getenv

import json

class TestActualizarEstadoDteReal(AbstractDteFacturacion):
    """
    Clase de pruebas para actualizar el estado de un DTE emitido (real).
    """

    @classmethod
    def setUpClass(cls):
        """
        Método para inicialización de variables y clases a utilizar.
        """
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(ApiClient.AMBIENTE_SII_PRUEBAS)

    def test_actualizar_estado_dte_real(self):
        """
        Método de test para actualizar el estado de un DTE.
        """
        try:
            # Se llama al método del abstract para listar DTEs reales.
            documentos = self._listar_dtes_reales(self.contribuyente_rut)
            # Se convierte en diccionario el resultado de la búsqueda.
            documentos_dict = documentos.json()

            # Filtros a utilizar.
            filtros = {
                'usarWebservice': 1
            }
            # Se intenta actualizar el estado del DTE real.
            response = self.dte.dte_emitidos_actualizar_estado(
                documentos_dict[0]['dte'],
                documentos_dict[0]['folio'],
                self.contribuyente_rut,
                filter = filtros
            )
            # Se asegura que el codigo sea 200.
            self.assertEqual(response.status_code, 200)
            # Si verbose es True, se despliega en pantalla el resultado.
            if self.verbose:
                print(
                    'test_actualizar_estado_dte_real() estado: ',
                    json.dumps(response.json())
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception o si el código no es 200.
            self.fail('ApiException: %(e)s' % {'e' : e})