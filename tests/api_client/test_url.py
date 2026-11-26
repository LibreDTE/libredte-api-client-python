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

"""
Pruebas de la URL que arma el cliente para cada solicitud, sin red.

    python tests/run.py api_client.test_url
"""

import base64
import os
import unittest
from unittest.mock import Mock, patch
from urllib.parse import ParseResult, parse_qs, urlparse

import requests

from libredte.api_client import ApiClient, ApiException
from libredte.api_client.cobros import Cobros
from libredte.api_client.dte import Dte
from libredte.api_client.sistema import Moneda

REQUEST = 'libredte.api_client.requests.Session.request'
HASH = '0' * 32
URL = 'https://libredte.invalid'


class TestUrl(unittest.TestCase):

    """Ruta y parámetros de la URL de las solicitudes."""

    def setUp(self) -> None:
        """Prepara una respuesta exitosa, sin variables de entorno."""
        entorno = patch.dict(os.environ, {}, clear=True)
        entorno.start()
        self.addCleanup(entorno.stop)
        self.response = Mock(spec=requests.Response)
        self.response.status_code = 200

    def url_solicitada(self, request: Mock) -> ParseResult:
        """Obtiene la URL con que se llamó a requests.request."""
        url: object = request.call_args.args[1]
        if not isinstance(url, str):
            self.fail(f'La URL solicitada no es un texto: {url!r}')
        return urlparse(url)

    def test_filtro_vacio_se_envia(self) -> None:
        """Un filtro con valor vacío se mantiene en la URL."""
        with patch(REQUEST, return_value=self.response) as request:
            Dte(HASH, URL).get_dte_real(33, 1, 76192083, {'formato': ''})
        url = self.url_solicitada(request)
        self.assertEqual(url.path, '/api/dte/dte_emitidos/info/33/1/76192083')
        self.assertEqual(
            parse_qs(url.query, keep_blank_values=True),
            {'formato': [''], '_version': ['v1']},
        )

    def test_filtros_booleanos_como_1_y_0(self) -> None:
        """Los booleanos se envían como 1 y 0: "False" es verdadero en PHP."""
        with patch(REQUEST, return_value=self.response) as request:
            Dte(HASH, URL).emitir_dte_real(
                {'dte': 33},
                {'email': False, 'normalizar': True},
            )
        query = parse_qs(self.url_solicitada(request).query)
        self.assertEqual(query['email'], ['0'])
        self.assertEqual(query['normalizar'], ['1'])

    def test_valores_de_la_ruta_se_escapan(self) -> None:
        """Un '+' de un código base64 no llega al servidor como espacio."""
        with patch(REQUEST, return_value=self.response) as request:
            Cobros(HASH, URL).get_cobro_info('ab+c=', 76192083)
        self.assertEqual(
            self.url_solicitada(request).path,
            '/api/pagos/cobros/info/ab%2Bc%3D/76192083',
        )

    def test_valor_que_cambia_la_ruta_se_rechaza(self) -> None:
        """Un valor no puede llevar la solicitud a otro recurso de la API."""
        dte = Dte(HASH, URL)
        for codigo in (
            '../../../../dte_emitidos/eliminar/33/10',
            '..',
            '.',
            '',
            'a/b',
        ):
            with (
                self.subTest(codigo=codigo),
                patch(REQUEST, return_value=self.response) as request,
            ):
                with self.assertRaises(ApiException):
                    dte.get_dte_temporal(1, 33, codigo, 76192083)
                request.assert_not_called()

    def test_url_base_con_barra_final(self) -> None:
        """Una URL base terminada en '/' no genera '//' en la ruta."""
        with patch(REQUEST, return_value=self.response) as request:
            Dte(HASH, URL + '/').get_xml_dte_real(33, 1, 76192083)
        self.assertEqual(
            self.url_solicitada(request).path,
            '/api/dte/dte_emitidos/xml/33/1/76192083',
        )

    def test_datos_vacios_se_envian(self) -> None:
        """Un objeto vacío se envía como {} (la API espera un objeto JSON)."""
        with patch(REQUEST, return_value=self.response) as request:
            Dte(HASH, URL).get_dte_emitidos(76192083, {})
        self.assertEqual(request.call_args.kwargs['data'], '{}')

    def test_tasa_de_cambio_sin_fecha(self) -> None:
        """Sin fecha, la ruta no la incluye y la API usa la fecha de hoy."""
        with patch(REQUEST, return_value=self.response) as request:
            Moneda(HASH, URL).get_moneda_cambios('CLP')
        self.assertEqual(
            self.url_solicitada(request).path,
            '/api/sistema/general/moneda_cambios/tasa/USD/CLP',
        )


class TestCreateLink(unittest.TestCase):

    """Enlaces a la plataforma web de LibreDTE."""

    def setUp(self) -> None:
        """Prepara un cliente sin variables de entorno."""
        entorno = patch.dict(os.environ, {}, clear=True)
        entorno.start()
        self.addCleanup(entorno.stop)
        self.client = ApiClient(HASH, URL)

    def test_rut_con_digito_verificador(self) -> None:
        """Acepta el RUT con dígito verificador, como set_contribuyente."""
        self.assertEqual(
            self.client.create_link(None, '76.192.083-9'),
            f'{URL}/dte/contribuyentes/seleccionar/76192083',
        )

    def test_url_base_con_barra_final(self) -> None:
        """Una URL base terminada en '/' no genera '//' en el enlace."""
        client = ApiClient(HASH, URL + '/')
        self.assertEqual(
            client.create_link(None, 76192083),
            f'{URL}/dte/contribuyentes/seleccionar/76192083',
        )

    def test_recurso_en_base64_se_escapa(self) -> None:
        """El '+' del base64 se escapa para no llegar como espacio."""
        recurso = '>>>'
        recurso_base64 = base64.b64encode(recurso.encode()).decode()
        self.assertIn('+', recurso_base64)
        self.assertEqual(
            self.client.create_link(recurso, 76192083),
            f'{URL}/dte/contribuyentes/seleccionar/76192083/'
            + recurso_base64.replace('+', '%2B'),
        )

    def test_rut_explicito_invalido_no_usa_el_configurado(self) -> None:
        """Un RUT explícito vacío o 0 falla en vez de usar self.rut."""
        self.client.set_contribuyente(76192083)
        for rut_invalido in ('', 0, False, -1, '76192083-'):
            with (
                self.subTest(rut_invalido=rut_invalido),
                self.assertRaises(ApiException),
            ):
                self.client.create_link('/dte/dte_emitidos', rut_invalido)


if __name__ == '__main__':
    unittest.main(verbosity=2)
