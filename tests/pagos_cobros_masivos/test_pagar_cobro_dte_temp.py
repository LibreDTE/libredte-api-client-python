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

from tests.pagos_cobros_masivos.abstract_pagos_cobros_masivos import AbstractPagosCobrosMasivos

from libredte.api_client import ApiException

from datetime import datetime
from os import getenv

import json

class TestPagarCobroDteTemp(AbstractPagosCobrosMasivos):
    """
    Clase de pruebas para pagar cobros de DTEs temporales.
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

    def test_pagar_cobro_dte_temp(self):
        """
        Método de test para pagar un cobro asociado a un DTE temporal.
        """
        try:
            # Se llama al método del abstract para buscar un cobro específico
            # de un DTE temporal.
            response_cobro = self._buscar_cobro_dte_temp(
                self.contribuyente_rut,
                self.datos
            )
            # Se pasan los datos del response a un diccionario.
            cobro_dict = response_cobro.json()
            # Datos de pago.
            data = {
                'medio': 'efectivo',
                'fecha': datetime.now().strftime('%Y-%m-%d')
            }
            # Se intenta pagar el cobro.
            response = self.cobros.pagar_cobro(
                cobro_dict['codigo'],
                self.contribuyente_rut,
                data
            )

            # Se asegura que el codigo sea 200.
            self.assertEqual(response.status_code, 200)

            # Si verbose es True, se despliega en pantalla el resultado.
            if self.verbose:
                print(
                    'test_pagar_cobro_dte_temp() cobro: ',
                    json.dumps(response.json())
                )
        except ApiException as e:
            # Falla si se obtiene error de API Exception o si el código no es 200.
            self.fail('ApiException: %(e)s' % {'e' : e})