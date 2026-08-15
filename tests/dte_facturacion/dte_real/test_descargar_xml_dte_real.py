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

from datetime import datetime
from base64 import b64decode
from os import getenv

import os

class TestDescargarXmlDteReal(AbstractDteFacturacion):
    """
    Clase de prueebas para descargar un XML de un DTE real.
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

    def test_descargar_xml_dte_real(self):
        """
        Método de test para descargar un XML asociado a un DTE real.

        IMPORTANTE: Se necesita tener un DTE real (emitido) para esta prueba.
        """
        try:
            # Se llama al método del abstract para emitir un DTE real.
            dte_temp = self._listar_dtes_reales(self.contribuyente_rut)
            # Se convierte en diccionario el resultado de la búsqueda.
            dte_dict = dte_temp.json()

            # Se descarga el XML del DTE real.
            response = self.dte.get_xml_dte_real(
                dte_dict[0]['dte'],
                dte_dict[0]['folio'],
                dte_dict[0]['emisor']
            )

            # Retrocede dos niveles para salir de 'dte_facturacion' y entrar en 'tests'
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            # Define la carpeta de destino correcta
            output_dir = os.path.join(base_dir, 'archivos', 'dte_facturacion', 'dte_real_xml')

            # Crear la carpeta si no existe
            os.makedirs(output_dir, exist_ok=True)

            # Generar la ruta y nombre del archivo. El nombre tiene el siguiente formato:
            # LIBREDTE_[rut_emisor]_[dte]_[folio].xml
            filename = os.path.join(
                output_dir,
                'LIBREDTE_%(rut)s_%(dte)s_%(folio)s.xml' % {
                    'rut' : dte_dict[0]['emisor'],
                    'dte' : dte_dict[0]['dte'],
                    'folio' : dte_dict[0]['folio']
                }
            )

            # Se asegura que el codigo sea 200.
            self.assertEqual(response.status_code, 200)

            # Se genera el XML con el nombre previamente definido, y el
            # contenido del response.
            with open(filename, 'wb') as f:
                f.write(b64decode(response.content))

            # Si verbose es True, se despliega en pantalla el resultado.
            if self.verbose:
                print(
                    'test_descargar_xml_dte_real() filename: ',
                    filename
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception o si el código no es 200.
            self.fail('ApiException: %(e)s' % {'e' : e})