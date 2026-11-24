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
Pruebas de la configuración de la conexión de ApiClient, sin red.

    python tests/run.py api_client.test_conexion
"""

import os
import socket
import threading
import time
import unittest
import warnings
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import ClassVar, override
from unittest.mock import Mock, patch

import requests

from libredte.api_client import ApiClient, ApiException
from libredte.api_client.dte import Dte

REQUEST = 'libredte.api_client.requests.Session.request'
HASH = '0' * 32
URL = 'https://libredte.invalid'


class TestConexion(unittest.TestCase):

    """Timeout, redirecciones y uso de HTTPS."""

    def setUp(self) -> None:
        """Prepara una respuesta exitosa, sin variables de entorno."""
        entorno = patch.dict(os.environ, {}, clear=True)
        entorno.start()
        self.addCleanup(entorno.stop)
        self.response = Mock(spec=requests.Response)
        self.response.status_code = 200

    def test_timeout_por_defecto(self) -> None:
        """Sin timeout, una falla de red dejaría la solicitud esperando."""
        with patch(REQUEST, return_value=self.response) as request:
            ApiClient(HASH, URL).get('dte/contribuyentes/info/1')
        self.assertEqual(request.call_args.kwargs['timeout'], (10, 300))

    def test_timeout_configurable(self) -> None:
        """Los wrappers permiten cambiar o desactivar el timeout."""
        for timeout in (5, (3, 60), None):
            with (
                self.subTest(timeout=timeout),
                patch(REQUEST, return_value=self.response) as request,
            ):
                Dte(HASH, URL, api_timeout=timeout).get_xml_dte_real(33, 1, 2)
                self.assertEqual(request.call_args.kwargs['timeout'], timeout)

    def test_redireccion_es_error(self) -> None:
        """Una redirección no se sigue: un POST perdería sus datos."""
        location = 'https://libredte.cl/api/dte/documentos/emitir'
        self.response.status_code = 301
        self.response.headers = {'Location': location}
        with (
            patch(REQUEST, return_value=self.response) as request,
            self.assertRaises(ApiException) as contexto,
        ):
            ApiClient(HASH, URL).post('dte/documentos/emitir', {'dte': 33})
        self.assertIs(request.call_args.kwargs['allow_redirects'], False)
        self.assertEqual(contexto.exception.code, 301)
        self.assertIn(location, contexto.exception.message)

    def test_redireccion_sin_raise_for_status(self) -> None:
        """Con raise_for_status=False se entrega la redirección."""
        self.response.status_code = 302
        self.response.headers = {'Location': f'{URL}/otra'}
        with patch(REQUEST, return_value=self.response):
            response = ApiClient(HASH, URL, raise_for_status=False).get('x')
        self.assertIs(response, self.response)

    def test_aviso_si_la_url_no_usa_https(self) -> None:
        """Con http:// el hash viaja sin cifrar: se avisa."""
        with self.assertWarns(UserWarning):
            ApiClient(HASH, 'http://libredte.cl')

    def test_sin_aviso_en_https_o_servidor_local(self) -> None:
        """HTTPS y servidores locales (desarrollo) no generan aviso."""
        for url in (URL, 'http://localhost:8080', 'http://127.0.0.1'):
            with (
                self.subTest(url=url),
                warnings.catch_warnings(record=True) as avisos,
            ):
                warnings.simplefilter('always')
                ApiClient(HASH, url)
                self.assertEqual(avisos, [])



class _Servidor(BaseHTTPRequestHandler):

    """Servidor HTTP local de prueba (responde según la ruta)."""

    # Cabecera Cookie recibida en cada solicitud
    cookies: ClassVar[list[str | None]] = []

    @override
    def log_request(
        self,
        code: int | str = '-',
        size: int | str = '-',
    ) -> None:
        """No muestra el registro de las solicitudes."""

    def do_GET(self) -> None:
        """Responde JSON, después de 1 segundo si la ruta es /api/lento."""
        _Servidor.cookies.append(self.headers.get('Cookie'))
        if self.path.startswith('/api/lento'):
            time.sleep(1)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Set-Cookie', 'PHPSESSID=abc; Path=/')
        self.end_headers()
        self.wfile.write(b'{}')


class TestSesionReal(unittest.TestCase):

    """Sesión HTTP real contra servidores locales (127.0.0.1)."""

    def setUp(self) -> None:
        """Inicia un servidor HTTP local, sin variables de entorno."""
        entorno = patch.dict(os.environ, {}, clear=True)
        entorno.start()
        self.addCleanup(entorno.stop)
        _Servidor.cookies = []
        servidor = ThreadingHTTPServer(('127.0.0.1', 0), _Servidor)
        threading.Thread(target=servidor.serve_forever, daemon=True).start()
        self.addCleanup(servidor.server_close)
        self.addCleanup(servidor.shutdown)
        self.url = f'http://127.0.0.1:{servidor.server_address[1]}'

    def test_timeout_de_lectura(self) -> None:
        """Un servidor que no responde a tiempo es un error de timeout."""
        client = ApiClient(HASH, self.url, timeout=(1, 0.2))
        with self.assertRaises(ApiException) as contexto:
            client.get('lento')
        self.assertTrue(
            contexto.exception.message.startswith('Error de timeout:'),
            contexto.exception.message,
        )

    def test_no_envia_cookies(self) -> None:
        """Cada solicitud es independiente: no se reenvían cookies."""
        client = ApiClient(HASH, self.url)
        client.get('uno')
        client.get('dos')
        self.assertEqual(_Servidor.cookies, [None, None])

    def test_no_repite_una_solicitud_que_llego(self) -> None:
        """Si la solicitud llegó y se cortó, no se repite (podría emitir)."""
        conexiones: list[int] = []
        escucha = socket.socket()
        escucha.bind(('127.0.0.1', 0))
        escucha.listen()
        self.addCleanup(escucha.close)

        def cortar() -> None:
            """Acepta las conexiones y las cierra sin responder."""
            while True:
                try:
                    conexion, _ = escucha.accept()
                except OSError:
                    return
                conexiones.append(1)
                conexion.recv(1024)
                conexion.close()

        threading.Thread(target=cortar, daemon=True).start()
        url = f'http://127.0.0.1:{escucha.getsockname()[1]}'
        with self.assertRaises(ApiException):
            ApiClient(HASH, url).post('dte/documentos/emitir', {'dte': 33})
        self.assertEqual(len(conexiones), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
