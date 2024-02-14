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

from os import getenv
import requests
import urllib
import json
from abc import ABC
import base64
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

class ApiClient:
    """
    Cliente API para integrarse con LibreDTE.

    Esta clase proporciona funcionalidades para interactuar con los servicios web de LibreDTE,
    permitiendo realizar operaciones GET y POST, y crear enlaces a recursos de LibreDTE.

    :param str url: URL base del servicio de LibreDTE.
    :param requests.auth.HTTPBasicAuth http_auth: Autenticación para las solicitudes HTTP.
    :param bool ssl_check: Indica si se debe verificar el certificado SSL del host.
    :param int rut: RUT del contribuyente en LibreDTE.
    """

    __DEFAULT_URL = 'https://libredte.cl'
    __DEFAULT_VERSION = 'v1'

    AMBIENTE_SII_PRODUCCION = 0
    AMBIENTE_SII_PRUEBAS = 1

    def __init__(self, hash=None, url=None, version=None, raise_for_status=True):
        """
        Inicializa el cliente API con la configuración necesaria para realizar las solicitudes.

        :param str hash: Hash de autenticación del usuario. Si es None, se intentará obtener de la variable de entorno LIBREDTE_HASH.
        :param str url: URL base del servicio de LibreDTE. Si es None, se intentará obtener de la variable de entorno LIBREDTE_URL o se usará la URL por defecto.
        :param str version: Versión de la API a utilizar. Por defecto, se usa una versión predefinida.
        :param bool raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
        :raises ApiException: Si el hash del usuario no es válido o está ausente.
        """
        username = self.__validate_hash(hash)
        password = 'X'
        self.url = self.__validate_url(url)
        self.headers = self.__generate_headers()
        self.version = version or self.__DEFAULT_VERSION
        self.raise_for_status = raise_for_status
        self.http_auth = requests.auth.HTTPBasicAuth(username, password)
        self.set_ssl()
        self.set_contribuyente()
        self.set_ambiente_sii()

    def __validate_hash(self, hash):
        """
        Valida y retorna el hash de autenticación.

        :param str hash: Hash de autenticación a validar.
        :return: Hash validado.
        :rtype: str
        :raises ApiException: Si el hash no es válido o está ausente.
        """
        hash = hash or getenv('LIBREDTE_HASH')
        if not hash:
            raise ApiException('Se debe configurar la variable de entorno: LIBREDTE_HASH.')
        hash = str(hash).strip()
        if len(hash) != 32:
            raise ApiException('El hash del usuario debe ser de 32 caracteres.')
        return hash

    def __validate_url(self, url):
        """
        Valida y retorna la URL base para la API.

        :param str url: URL a validar.
        :return: URL validada.
        :rtype: str
        :raises ApiException: Si la URL no es válida o está ausente.
        """
        return str(url).strip() if url else getenv('LIBREDTE_URL', self.__DEFAULT_URL).strip()

    def __generate_headers(self):
        """
        Genera y retorna las cabeceras por defecto para las solicitudes.

        :return: Cabeceras por defecto.
        :rtype: dict
        """
        return {
            'User-Agent': 'LibreDTE: Cliente de API en Python.',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def set_ssl(self, ssl_check=True):
        """
        Configura las opciones de SSL para las conexiones HTTP.

        Este método permite activar o desactivar la verificación del certificado SSL
        del servidor. Si se activa, las conexiones HTTP verificarán el certificado SSL
        del servidor; si se desactiva, no lo harán.

        :param bool ssl_check: Indica si se debe verificar el certificado SSL del host. Por defecto es True.

        :return: El estado actualizado de la verificación del SSL.
        :rtype: bool

        Ejemplo de uso:
            client.set_ssl(False)  # Desactiva la verificación SSL
        """
        self.ssl_check = ssl_check
        return self.ssl_check

    def set_contribuyente(self, rut=None):
        """
        Establece el RUT del contribuyente para las solicitudes de la API.

        Este método permite configurar el RUT del contribuyente que se utilizará en las
        solicitudes subsiguientes. Si se proporciona un RUT, este se utiliza; de lo contrario,
        se intenta obtener de la variable de entorno 'LIBREDTE_RUT'.

        :param rut: RUT del contribuyente a establecer. Si es None, se intentará obtener
                    de la variable de entorno 'LIBREDTE_RUT'.
        :type rut: int, str, optional
        :return: El RUT del contribuyente configurado.
        :rtype: int
        :raises ApiException: Si el RUT es inválido o no se puede convertir a entero.
        """
        rut = rut or getenv('LIBREDTE_RUT')
        if rut is not None:
            if isinstance(rut, str) and '-' in rut:
                rut = rut.replace('.', '').split('-')[0]
            try:
                rut = int(rut)
            except ValueError:
                raise ApiException(f'Valor de RUT inválido: {rut}')
        self.rut = rut
        return self.rut

    def set_ambiente_sii(self, ambiente=None):
        """
        Establece el ambiente del Servicio de Impuestos Internos (SII) para las solicitudes de la API.

        Este método permite configurar el ambiente (producción o pruebas) que se utilizará en las
        solicitudes subsiguientes. El ambiente se puede especificar directamente o ser obtenido
        de la variable de entorno 'LIBREDTE_AMBIENTE'. Los valores válidos son identificadores
        para producción ('0', 'produccion', 'prod', 'palena') y pruebas ('1', 'pruebas', 'test', 'maullin').

        :param str ambiente: Identificador del ambiente a establecer. Si es None, se intentará obtener
                             de la variable de entorno 'LIBREDTE_AMBIENTE'.
        :return: El ambiente del SII configurado.
        :rtype: str
        :raises ApiException: Si el valor proporcionado para el ambiente es inválido.
        """
        ambiente = ambiente if ambiente is not None else getenv('LIBREDTE_AMBIENTE')
        if ambiente == '':
            ambiente = None
        if ambiente is not None:
            ambiente = str(ambiente).strip()
            if ambiente in ('0', 'produccion', 'prod', 'palena'):
                ambiente = self.AMBIENTE_SII_PRODUCCION
            elif ambiente in ('1', 'pruebas',  'test', 'maullin'):
                ambiente = self.AMBIENTE_SII_PRUEBAS
            else:
                raise ApiException(f'Valor de Ambiente SII inválido: {ambiente}')
        self.ambiente_sii = ambiente
        return self.ambiente_sii

    def get(self, resource, headers=None):
        """
        Realiza una solicitud GET a un recurso de la API de LibreDTE.

        :param str resource: Recurso de la API que se desea consumir.
        :param dict headers: Cabeceras adicionales para la solicitud. Si es None, se usarán las cabeceras por defecto.
        :return: Objeto de respuesta de la solicitud HTTP.
        :rtype: requests.Response
        :raises ApiException: Lanza una excepción si ocurre un error en la solicitud HTTP, como errores de conexión, timeout o HTTP.
        """
        return self.__request('GET', resource, headers=headers)

    def post(self, resource, data=None, headers=None):
        """
        Realiza una solicitud POST a un recurso de la API de LibreDTE.

        :param str resource: Recurso de la API que se desea consumir.
        :param dict, str data: Datos que se enviarán con la solicitud. Si es un diccionario, se codificará como JSON.
        :param dict headers: Cabeceras adicionales para la solicitud. Si es None, se usarán las cabeceras por defecto.
        :return: Objeto de respuesta de la solicitud HTTP.
        :rtype: requests.Response
        :raises ApiException: Lanza una excepción si ocurre un error en la solicitud HTTP, como errores de conexión, timeout o HTTP.
        """
        return self.__request('POST', resource, data, headers)

    def __request(self, method, resource, data=None, headers=None):
        """
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si el método HTTP no es soportado o si hay un error de conexión.
        """
        api_path = f'/api/{resource}'
        full_url = urllib.parse.urljoin(self.url + '/', api_path.lstrip('/'))
        extra_params = {'_version': self.version}
        if self.rut is not None:
            extra_params['_contribuyente_rut'] = self.rut
        if self.ambiente_sii is not None:
            extra_params['_contribuyente_certificacion'] = self.ambiente_sii
        full_url = self.__add_parameters_to_url(full_url, extra_params)
        headers = headers or {}
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            try:
                data = json.dumps(data)
            except TypeError as e:
                raise ApiException(f'Error al codificar los datos en JSON: {e}')
        try:
            response = requests.request(
                method, full_url, data=data, headers=headers, auth=self.http_auth, verify=self.ssl_check
            )
            return self.__check_and_return_response(response)
        except requests.exceptions.ConnectionError as error:
            raise ApiException(f'Error de conexión: {error}')
        except requests.exceptions.Timeout as error:
            raise ApiException(f'Error de timeout: {error}')
        except requests.exceptions.RequestException as error:
            raise ApiException(f'Error en la solicitud: {error}')

    def __add_parameters_to_url(self, url, params):
        """
        Añade o actualiza parámetros en la URL dada.

        Esta función toma una URL y un diccionario de parámetros, y devuelve una nueva URL
        con los parámetros añadidos o actualizados. Si un parámetro ya existe en la URL,
        su valor se actualizará; si no existe, el parámetro se añadirá.

        :param str url: La URL original a la que se añadirán los parámetros.
        :param dict params: Un diccionario de parámetros y valores para añadir a la URL.
        :return: La URL con los parámetros añadidos o actualizados.
        :rtype: str
        """
        # Descomponer la URL en sus componentes
        parsed_url = urlparse(url)

        # Extraer y modificar los parámetros de query
        query_params = parse_qs(parsed_url.query)
        for key, value in params.items():
            query_params[key] = value

        # Reconstruir la query string
        new_query_string = urlencode(query_params, doseq=True)

        # Reconstruir la URL completa
        new_url = urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment)
        )

        return new_url

    def __check_and_return_response(self, response):
        """
        Verifica la respuesta de la solicitud HTTP y maneja los errores.

        :param requests.Response response: Objeto de respuesta de requests.
        :return: Respuesta validada.
        :rtype: requests.Response
        :raises ApiException: Si la respuesta contiene un error HTTP.
        """
        if response.status_code != 200 and self.raise_for_status:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                try:
                    body = error.response.json()
                    error_message = body if isinstance(body, str) else body.get(
                        'message', 'Error desconocido.'
                    )
                except json.decoder.JSONDecodeError:
                    error_message = f'Error al decodificar los datos en JSON: {error.response.text}'
                raise ApiException(error_message, response.status_code)
        return response

    def create_link(self, resource, rut = None):
        """
        Crea un enlace que apunta a un recurso específico en la plataforma de LibreDTE.

        :param str resource: Recurso al que se desea acceder en la plataforma de LibreDTE.
        :param int rut: RUT del contribuyente en LibreDTE con el que se quiere usar el recurso. Si es None, se usará el RUT almacenado en la clase.
        :return: URL formada para acceder al recurso especificado.
        :rtype: str
        """
        rut = rut or self.rut
        try:
            if rut is None:
                raise ValueError()
            rut = int(rut)
        except ValueError:
            raise ApiException(f'Valor de RUT inválido: {rut}')
        if resource:
            resource_base64 = base64.b64encode(resource.encode('utf-8')).decode('utf-8')
            link = f'{self.url}/dte/contribuyentes/seleccionar/{rut}/{str(resource_base64)}'
        else:
            link = f'{self.url}/dte/contribuyentes/seleccionar/{rut}'
        return link

class ApiException(Exception):
    """
    Excepción personalizada para errores en el cliente de la API.

    :param str message: Mensaje de error.
    :param int code: Código de error (opcional).
    :param dict params: Parámetros adicionales del error (opcional).
    """

    def __init__(self, message, code=None, params=None):
        self.message = message
        self.code = code
        self.params = params
        super().__init__(message)

    def __str__(self):
        """
        Devuelve una representación en cadena del error, proporcionando un contexto claro
        del problema ocurrido. Esta representación incluye el prefijo "[LibreDTE]",
        seguido del código de error si está presente, y el mensaje de error.

        Si se especifica un código de error, el formato será:
        "[LibreDTE] Error {code}: {message}"

        Si no se especifica un código de error, el formato será:
        "[LibreDTE] {message}"

        :return: Una cadena que representa el error de una manera clara y concisa.
        """
        if self.code is not None:
            return f"[LibreDTE] Error {self.code}: {self.message}"
        else:
            return f"[LibreDTE] {self.message}"

class ApiBase(ABC):
    """
    Clase base para las clases que consumen la API (wrappers).

    :param str api_hash: Hash de autenticación del usuario. Si es None, se intentará obtener de la variable de entorno LIBREDTE_HASH.
    :param str api_url: URL base del servicio de LibreDTE. Si es None, se intentará obtener de la variable de entorno LIBREDTE_URL o se usará la URL por defecto.
    :param str api_version: Versión de la API a utilizar. Por defecto, se usa una versión predefinida.
    :param bool api_raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
    :param dict kwargs: Argumentos adicionales para la autenticación.
    """

    def __init__(self, api_hash=None, api_url=None, api_version=None, api_raise_for_status=True, **kwargs):
        self.client = ApiClient(api_hash, api_url, api_version, api_raise_for_status)
