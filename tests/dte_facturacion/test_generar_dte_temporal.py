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
from libredte.api_client.cobros import Cobros

class TestGenerarDteTemporal(unittest.TestCase):

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
        cls.cobros = Cobros()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(cls.dte.client.AMBIENTE_SII_PRUEBAS)

    def _buscar_temp(self):
        filtros = {
            'fecha_desde': '2015-01-01',
            'fecha_hasta': datetime.now().strftime("%Y-%m-%d"),
        }
        response = self.dte.listar_dtes_temporales(self.contribuyente_rut, filtros)
        return response.json()

    def test_dte_temp_generar(self):
        lista_dtes = self._listar_dtes_temporales()
        dte_temporal = self._emitir_dte_temporal()
        info_dte = self._buscar_documento_temp(lista_dtes)
        self._descargar_pdf_temp(dte_temporal)
        cobro = self._buscar_cobro_asociado_dte_temp(dte_temporal)
        self._eliminar_dte_temp(dte_temporal)

    def _listar_dtes_temporales(self):
        filtros = {
            'fecha_desde': '2015-01-01',
            'fecha_hasta': datetime.now().strftime("%Y-%m-%d"),
        }
        response = self.dte.listar_dtes_temporales(self.contribuyente_rut, filtros)
        return response.json()

    def _emitir_dte_temporal(self):
        try:
            response = self.dte.emitir_dte_temporal(self.datos)
            dte_temporal = response.json()
            if self.verbose:
                print('test_dte_temp_generar(): dte_temporal', json.dumps(dte_temporal))
            return dte_temporal
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def _buscar_documento_temp(self, lista_dte):
        try:
            dtes = lista_dte[0]
            response = self.dte.get_dte_temporal(dtes['receptor'], dtes['dte'], dtes['codigo'], self.contribuyente_rut)
            documento = response.json()

            self.assertTrue(True)
            if self.verbose:
                dte_id = f"T{documento['dte']}F{documento['codigo']}"
                print(f'\ntest_dte_temp_buscar_documento() dte_id {dte_id}\n')
                print(f"\ntest_dte_temp_buscar_documento() dte_fecha {documento['fecha']}\n")
                print(f"\ntest_dte_temp_buscar_documento() dte_total {documento['total']}\n")
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def _descargar_pdf_temp(self, dte_temporal):
        try:
            response = self.dte.get_pdf_temporal(dte_temporal['receptor'], dte_temporal['dte'], dte_temporal['codigo'], self.contribuyente_rut)
            filename = os.path.join(
                os.path.dirname(__file__),
                os.path.basename(__file__).replace('.py', '.pdf')
            )
            with open(filename, 'wb') as f:
                f.write(response.content)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_dte_temp_generar(): filename', filename)
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def _buscar_cobro_asociado_dte_temp(self, dte_temporal):
        try:
            response = self.cobros.get_cobro_dte_temporal(dte_temporal['receptor'], dte_temporal['dte'], dte_temporal['codigo'], dte_temporal['emisor'])
            cobro = response.json()

            self.assertEqual(response.status_code, 200)
            if self.verbose:
                print(f"\ntest_dte_temp_generar() cobro_dte_temp {response.content}\n")
            return cobro
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    def _eliminar_dte_temp(self, dte_temporal):
        try:
            response = self.dte.delete_dte_temporal(dte_temporal['receptor'], dte_temporal['dte'], dte_temporal['codigo'], dte_temporal['emisor'])

            self.assertEqual(response.status_code, 200)
            if self.verbose:
                print(f"\ntest_dte_temp_generar() eliminar_dte_temp {response.content}\n")
        except ApiException as e:
            self.fail(f"ApiException: {e}")