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

class TestDescargarXmlDteTemp(AbstractDteFacturacion):
    """
    Clase de prueebas para descargar un XML de un DTE temporal.
    """

    # Diccionario de datos de un DTE para emitir.
    datos = {
        'Encabezado': {
            'IdDoc': {
                'TipoDTE': 33,
                'FchEmis': None, # se reemplaza al preparar la clase
            },
            'Emisor': {
                'RUTEmisor': None # se reemplaza al preparar la clase
            },
            'Receptor': {
                'RUTRecep': '60803000-K',
                'RznSocRecep': 'Servicio de Impuestos Internos (SII)',
                'GiroRecep': 'Administración Pública',
                'Contacto': '+56 2 3252 5575',
                'CorreoRecep': 'facturacionmipyme@sii.cl',
                'DirRecep': 'Teatinos 120',
                'CmnaRecep': 'Santiago',
            }
        },
        'Detalle': [
            {
                #'IndExe': 1, # para items exentos
                'NmbItem': 'Asesoría de LibreDTE',
                'QtyItem': 1,
                'PrcItem': 1000,
            }
        ],
        'Referencia': [
            {
                'TpoDocRef': 801,
                'FolioRef': 'OC123',
                'FchRef': '2015-10-01',
            }
        ],
    }

    @classmethod
    def setUpClass(cls):
        """
        Método de inicialización de variables y clases a utilizar.
        """
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        fecha_emision = getenv('TEST_DTE_FACTURAR_FECHA_EMISION', datetime.now().strftime('%Y-%m-%d')).strip()
        cls.datos['Encabezado']['IdDoc']['FchEmis'] = fecha_emision
        cls.datos['Encabezado']['Emisor']['RUTEmisor'] = cls.contribuyente_rut
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(cls.dte.client.AMBIENTE_SII_PRUEBAS)

    def test_descargar_xml_dte_temp(self):
        """
        Método de test para descargar un XML asociado a un DTE temporal.
        """
        try:
            # Se llama al método del abstract para emitir un DTE temporal.
            dte_temp = self._emitir_dte_temporal(self.datos)
            # Se convierte en diccionario el resultado de la búsqueda.
            dte_dict = dte_temp.json()

            # Se descarga el XML del DTE temporal recién emitido.
            response = self.dte.get_xml_dte_temporal(
                dte_dict['receptor'],
                dte_dict['dte'],
                dte_dict['codigo'],
                dte_dict['emisor']
            )

            # Retrocede dos niveles para salir de 'dte_facturacion' y entrar en 'tests'
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            # Define la carpeta de destino correcta
            output_dir = os.path.join(base_dir, 'archivos', 'dte_facturacion', 'dte_temp_xml')

            # Crear la carpeta si no existe
            os.makedirs(output_dir, exist_ok=True)

            # Generar la ruta y nombre del archivo. El nombre tiene el siguiente formato:
            # LIBREDTE_[rut_emisor]_[dte]_[codigo].xml
            filename = os.path.join(
                output_dir,
                'LIBREDTE_%(rut)s_%(dte)s_%(codigo)s.xml' % {
                    'rut' : self.contribuyente_rut,
                    'dte' : dte_dict['dte'],
                    'codigo' : dte_dict['codigo']
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
                    'test_descargar_xml_dte_temp() filename: ',
                    filename
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception o si el código no es 200.
            self.fail('ApiException: %(e)s' % {'e' : e})