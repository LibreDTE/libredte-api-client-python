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

class TestBuscarDteRecibido(AbstractDteFacturacion):
    """
    Clase de pruebas para buscar un DTE recibido específico.
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

    def test_buscar_dte_recibido(self):
        """
        Método de test para obtener DTE recibido específico.
        """
        try:
            # Se llama al método del abstract para listar DTEs recibidos.
            dte_temp = self._listar_dtes_recibidos(self.contribuyente_rut)
            # Se convierte en diccionario el resultado de la búsqueda.
            dte_dict = dte_temp.json()

            # Si no hay documentos, arroja error ApiException.
            if len(dte_dict) == 0:
                raise ApiException(
                    'No se han encontrado documentos recibidos.',
                    404
                )

            # Se busca el DTE recibido buscado previamente.
            response = self.dte.get_dte_recibido(
                dte_dict[0]['emisor'],
                dte_dict[0]['dte'],
                dte_dict[0]['folio'],
                dte_dict[0]['receptor']
            )
            # Se asegura que el codigo sea 200.
            self.assertEqual(response.status_code, 200)
            # Si verbose es True, se despliega en pantalla el resultado.
            if self.verbose:
                print(
                    'test_buscar_dte_recibido() dte: ',
                    json.dumps(response.json())
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception o si el código no es 200.
            self.fail('ApiException: %(e)s' % {'e' : e})