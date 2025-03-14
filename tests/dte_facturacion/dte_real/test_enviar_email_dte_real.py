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

from datetime import datetime
from os import getenv

import json

class TestEnviarEmailDteReal(AbstractDteFacturacion):
    """
    Clase de pruebas para actualizar el estado de un DTE emitido (real).
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
        Método para inicialización de variables y clases a utilizar.
        """
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        cls.email = getenv('TEST_EMAIL')
        fecha_emision = getenv('TEST_DTE_FACTURAR_FECHA_EMISION', datetime.now().strftime('%Y-%m-%d')).strip()
        cls.datos['Encabezado']['IdDoc']['FchEmis'] = fecha_emision
        cls.datos['Encabezado']['Emisor']['RUTEmisor'] = cls.contribuyente_rut
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(ApiClient.AMBIENTE_SII_PRUEBAS)

    def test_enviar_email_dte_real(self):
        """
        Método de test para enviar un DTE emitido existente por correo.
        """
        try:
            # Se llama al método del abstract para listar DTEs reales.
            documentos = self._listar_dtes_reales(self.contribuyente_rut)
            # Se convierte en diccionario el resultado de la búsqueda.
            documentos_dict = documentos.json()
            # Datos del correo a enviar.
            datos_email = {
                'emails': [self.email],
                'asunto': '[LibreDTE API Client Test] Envío de DTE T%(dte)sF%(folio)s de %(rut)s' % {
                    'dte': documentos_dict[0]['dte'],
                    'folio': documentos_dict[0]['folio'],
                    'rut': self.contribuyente_rut
                },
                'mensaje': 'LibreDTE API Client Test: DTE ID T%(dte)sF%(folio)s de %(rut)s.' % {
                    'dte': documentos_dict[0]['dte'],
                    'folio': documentos_dict[0]['folio'],
                    'rut': self.contribuyente_rut
                },
                'pdf': True,
                'cedible': True,
                'papelContinuo': False,
            }# TODO: Revisar formato de comillas (estandarizar con comillas simples).
            # Se intenta enviar el correo con el DTE emitido.
            response = self.dte.dte_real_enviar_email(
                documentos_dict[0]['dte'],
                documentos_dict[0]['folio'],
                self.contribuyente_rut,
                datos_email
            )

            # Se asegura que el codigo sea 200.
            self.assertEqual(response.status_code, 200)
            # Si verbose es True, se despliega en pantalla el resultado.
            if self.verbose:
                print(
                    'test_enviar_email_dte_real() email: ',
                    json.dumps(response.json())
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception o si el código no es 200.
            self.fail('ApiException: %(e)s' % {'e' : e})
