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
from os import getenv, remove as file_remove
from datetime import datetime
import json
import os
from libredte.api_client import ApiException
from libredte.api_client.dte import Dte

class TestEmitirDocumento(unittest.TestCase):

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
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        fecha_emision = getenv('TEST_DTE_FACTURAR_FECHA_EMISION', datetime.now().strftime("%Y-%m-%d")).strip()
        cls.datos['Encabezado']['IdDoc']['FchEmis'] = fecha_emision
        cls.datos['Encabezado']['Emisor']['RUTEmisor'] = cls.contribuyente_rut
        cls.dte = Dte()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(cls.dte.client.AMBIENTE_SII_PRUEBAS)

    def test_dte_facturar(self):
        dte_temporal = self._emitir_dte_temporal()
        dte_emitido = self._generar_dte_emitido(dte_temporal) # AKA: dte real
        self._descargar_pdf(dte_emitido)

    def _emitir_dte_temporal(self):
        try:
            response = self.dte.emitir_dte_temporal(self.datos)
            dte_temporal = response.json()
            if self.verbose:
                print('test_dte_facturar(): dte_temporal', json.dumps(dte_temporal))
            return dte_temporal
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def _generar_dte_emitido(self, dte_temporal):
        try:
            response = self.dte.emitir_dte_real(dte_temporal)
            dte_emitido = response.json()
            if self.verbose:
                print('test_dte_facturar(): dte_emitido', json.dumps(dte_emitido))
            return dte_emitido
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def _descargar_pdf(self, dte_emitido):
        try:
            response = self.dte.get_pdf_real(dte_emitido['dte'], dte_emitido['folio'], dte_emitido['emisor'])
            filename = os.path.join(
                os.path.dirname(__file__),
                os.path.basename(__file__).replace('.py', '.pdf')
            )
            with open(filename, 'wb') as f:
                f.write(response.content)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_dte_facturar(): filename', filename)
        except ApiException as e:
            self.fail(f"ApiException: {e}")
