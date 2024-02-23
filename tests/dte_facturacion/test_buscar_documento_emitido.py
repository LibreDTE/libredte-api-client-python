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
from datetime import datetime
import base64
from libredte.api_client import ApiClient, ApiException
from libredte.api_client.contribuyentes import Contribuyentes
from libredte.api_client.cobros import Cobros
from libredte.api_client.dte import Dte

class TestBuscarDocumentoEmitido(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        cls.email = getenv('TEST_EMAIL')
        cls.dte = Dte()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(ApiClient.AMBIENTE_SII_PRUEBAS)

    def _buscar(self):
        filtros = {
            'fecha_desde': '2015-01-01',
            'fecha_hasta': datetime.now().strftime("%Y-%m-%d"),
        }
        response = self.dte.get_dte_emitidos(filtros)
        return response.json()

    def test_dte_buscar_documento_emitido(self):
        try:
            documentos = self._buscar()
            self.assertTrue(True)
            if self.verbose:
                dte_id = f"T{documentos[0]['dte']}F{documentos[0]['folio']}"
                print(f'\ntest_dte_buscar_documento_emitido() n_documentos {len(documentos)}\n')
                print(f'\ntest_dte_buscar_documento_emitido() dte_id {dte_id}\n')
                print(f"\ntest_dte_buscar_documento_emitido() dte_fecha {documentos[0]['fecha']}\n")
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def test_dte_estado(self):
        try:
            documentos = self._buscar()
            filtros = {
                'usarWebservice': 1
            }
            response = self.dte.dte_emitidos_actualizar_estado(documentos[0]["dte"], documentos[0]["folio"], self.contribuyente_rut, filter = filtros)
            self.assertEqual(response.status_code, 200)
            if self.verbose:
                dte_id = f'T{documentos[0]["dte"]}F{documentos[0]["folio"]}'
                print(f'\ntest_dte_estado() dte_id {dte_id}\n')
                print(f'\ntest_dte_estado() dte_estado {response.json()["revision_estado"]}\n')
        except ApiException as e:
            self.fail(f'ApiException: {e}')

    def test_dte_consultar(self):
        try:
            documentos = self._buscar()
            filtros = {
                'emisor': self.contribuyente_rut,
                'dte': documentos[0]['dte'],
                'folio': documentos[0]['folio'],
                'fecha': documentos[0]['fecha'],
                'total': documentos[0]['total'],
            }
            response = self.dte.dte_emitidos_consultar(filtros=filtros)
            self.assertEqual(response.status_code, 200)
            if self.verbose:
                dte_id = f'T{documentos[0]["dte"]}F{documentos[0]["folio"]}'
                print(f'\ntest_dte_consultar() dte_id {dte_id}\n')
                print(f'\ntest_dte_consultar() fecha_hora_creacion {response.json()["fecha_hora_creacion"]}\n')
        except ApiException as e:
            self.fail(f'ApiException: {e}')

    def test_dte_ted(self):
        try:
            documentos = self._buscar()
            formato = 'xml'  # Opciones: png (defecto), bmp, xml
            filtros = {
                'formato': formato
            }
            response = self.dte.dte_emitidos_ted(documentos[0]["dte"], documentos[0]["folio"], self.contribuyente_rut, filtros=filtros)
            self.assertEqual(response.status_code, 200)
            if self.verbose:
                dte_id = f'T{documentos[0]["dte"]}F{documentos[0]["folio"]}'
                print(f'\ntest_dte_ted() dte_id {dte_id}\n')
                print(f'\ntest_dte_ted() dte_ted {base64.b64decode(response.json())}\n')
        except ApiException as e:
            self.fail(f'ApiException: {e}')

    def test_dte_email(self):
        try:
            documentos = self._buscar()
            datos_email = {
                'emails': [self.email],
                'asunto': f'[LibreDTE API Client Test] Envío de DTE T{documentos[0]["dte"]}F{documentos[0]["folio"]} de {self.contribuyente_rut}',
                'mensaje': f'LibreDTE API Client Test: DTE ID T{documentos[0]["dte"]}F{documentos[0]["folio"]} de {self.contribuyente_rut}.',
                'pdf': True,
                'cedible': True,
                'papelContinuo': False,
            }
            response = self.dte.dte_real_enviar_email(documentos[0]["dte"], documentos[0]["folio"], self.contribuyente_rut, datos_email)
            self.assertEqual(response.status_code, 200)
            if self.verbose:
                dte_id = f'T{documentos[0]["dte"]}F{documentos[0]["folio"]}'
                print(f'\ntest_dte_email() dte_id {dte_id}\n')
                print(f'\ntest_dte_email() email {" ".join(response.json())}\n')
        except ApiException as e:
            self.fail(f'ApiException: {e}')
