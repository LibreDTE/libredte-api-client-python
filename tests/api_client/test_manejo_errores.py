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
Pruebas del manejo de errores de ApiClient, sin red.

Los errores de la solicitud (conexión, timeout) y las respuestas HTTP con
error se deben entregar como ApiException, con un mensaje claro.

    python tests/run.py api_client.test_manejo_errores
"""

import os
import unittest
from unittest.mock import Mock, patch

import requests

from libredte.api_client import ApiClient, ApiException

REQUEST = 'libredte.api_client.requests.Session.request'


def respuesta_con_error(status_code: int) -> Mock:
    """Respuesta HTTP con error, cuyo raise_for_status lanza HTTPError."""
    response = Mock(spec=requests.Response)
    response.status_code = status_code
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=response,
    )
    return response


class TestManejoDeErrores(unittest.TestCase):

    """Los errores de la API se entregan como ApiException."""

    def setUp(self) -> None:
        """Cliente con un hash válido, sin depender de las variables."""
        # Sin variables de entorno: LIBREDTE_RUT o LIBREDTE_AMBIENTE de quien
        # ejecuta las pruebas no deben afectar al cliente.
        entorno = patch.dict(os.environ, {}, clear=True)
        entorno.start()
        self.addCleanup(entorno.stop)
        self.client = ApiClient('0' * 32, 'https://libredte.invalid')

    def test_error_de_conexion(self) -> None:
        """Un error de conexión es ApiException, no TypeError."""
        error = requests.exceptions.ConnectionError('sin red')
        with (
            patch(REQUEST, side_effect=error),
            self.assertRaises(ApiException) as contexto,
        ):
            self.client.get('dte/contribuyentes/info/76192083')
        self.assertEqual(
            str(contexto.exception),
            '[LibreDTE] Error de conexión: sin red',
        )
        self.assertIs(contexto.exception.__cause__, error)

    def test_error_de_timeout(self) -> None:
        """Un timeout es ApiException con su propio mensaje."""
        error = requests.exceptions.Timeout('sin respuesta')
        with (
            patch(REQUEST, side_effect=error),
            self.assertRaises(ApiException) as contexto,
        ):
            self.client.post('dte/documentos/emitir', data={'dte': 33})
        self.assertEqual(
            str(contexto.exception),
            '[LibreDTE] Error de timeout: sin respuesta',
        )

    def test_timeout_de_conexion(self) -> None:
        """Un ConnectTimeout se informa como timeout, no como conexión."""
        error = requests.exceptions.ConnectTimeout('sin respuesta')
        with (
            patch(REQUEST, side_effect=error),
            self.assertRaises(ApiException) as contexto,
        ):
            self.client.get('dte/contribuyentes/info/76192083')
        self.assertEqual(
            str(contexto.exception),
            '[LibreDTE] Error de timeout: sin respuesta',
        )

    def test_datos_que_no_se_pueden_codificar(self) -> None:
        """Una referencia circular en los datos es ApiException."""
        datos: dict[str, object] = {}
        datos['propio'] = datos
        with (
            patch(REQUEST) as request,
            self.assertRaises(ApiException) as contexto,
        ):
            self.client.post('dte/documentos/emitir', data=datos)
        self.assertTrue(
            contexto.exception.message.startswith(
                'Error al codificar los datos en JSON:',
            ),
        )
        request.assert_not_called()

    def test_error_http_con_mensaje_json(self) -> None:
        """El mensaje es el campo 'message' del JSON y el código el HTTP."""
        response = respuesta_con_error(400)
        cuerpo = {'message': 'RUT inválido.', 'campo': 'rut'}
        response.json.return_value = cuerpo
        with (
            patch(REQUEST, return_value=response),
            self.assertRaises(ApiException) as contexto,
        ):
            self.client.get('dte/contribuyentes/info/1')
        self.assertEqual(contexto.exception.code, 400)
        self.assertEqual(contexto.exception.message, 'RUT inválido.')
        # El objeto JSON completo queda disponible en los parámetros
        self.assertEqual(contexto.exception.params, cuerpo)

    def test_error_http_sin_json(self) -> None:
        """Si el cuerpo no es JSON, el mensaje incluye el texto recibido."""
        response = respuesta_con_error(502)
        response.json.side_effect = requests.exceptions.JSONDecodeError(
            'Expecting value',
            '<html>Bad Gateway</html>',
            0,
        )
        response.text = '<html>Bad Gateway</html>'
        with (
            patch(REQUEST, return_value=response),
            self.assertRaises(ApiException) as contexto,
        ):
            self.client.get('dte/contribuyentes/info/1')
        self.assertEqual(contexto.exception.code, 502)
        self.assertEqual(
            contexto.exception.message,
            'Error al decodificar los datos en JSON: '
            '<html>Bad Gateway</html>',
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
