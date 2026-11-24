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
Cliente de la API de LibreDTE.

Incluye el cliente HTTP (:class:`ApiClient`), la excepción de la API
(:class:`ApiException`) y la clase base de los wrappers (:class:`ApiBase`).
"""

import base64
import json
import warnings
from collections.abc import Mapping, Sequence
from http import HTTPStatus
from http.cookiejar import DefaultCookiePolicy
from os import getenv
from typing import Literal, TypeIs
from urllib.parse import (
    parse_qs,
    quote,
    urlencode,
    urljoin,
    urlparse,
    urlunparse,
)

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util import Retry


class ApiClient:

    """
    Cliente API para integrarse con LibreDTE.

    Esta clase proporciona funcionalidades para interactuar con los servicios
    web de LibreDTE, permitiendo realizar operaciones GET y POST, y crear
    enlaces a recursos de LibreDTE.

    :ivar str url: URL base del servicio de LibreDTE.
    :ivar requests.auth.HTTPBasicAuth http_auth: Autenticación para las
        solicitudes HTTP.
    :ivar bool ssl_check: Indica si se debe verificar el certificado SSL del
        host.
    :ivar int rut: RUT del contribuyente en LibreDTE, o None si no se
        configuró.
    :ivar int ambiente_sii: Ambiente del SII (producción o pruebas), o None
        si no se configuró.
    :ivar timeout: Tiempo máximo de espera de las solicitudes, en segundos.
    :ivar requests.Session session: Sesión HTTP de las solicitudes (reutiliza
        las conexiones y reintenta si no logra conectarse).
    """

    __DEFAULT_URL = 'https://libredte.cl'
    __DEFAULT_VERSION = 'v1'
    __HASH_LENGTH = 32
    # Servidores locales (desarrollo), donde se acepta HTTP sin aviso
    __LOCAL_HOSTS = ('localhost', '127.0.0.1', '::1')

    # Tiempo máximo de espera por defecto, en segundos: para conectar y para
    # recibir la respuesta (hay operaciones lentas, como las que consultan
    # al SII)
    DEFAULT_TIMEOUT: tuple[float, float] = (10, 300)

    # Reintentos si no se logra conectar al servidor (la solicitud no llegó)
    CONNECT_RETRIES = 3

    AMBIENTE_SII_PRODUCCION = 0
    AMBIENTE_SII_PRUEBAS = 1

    http_auth: HTTPBasicAuth
    ssl_check: bool
    rut: int | None
    ambiente_sii: int | None
    session: requests.Session

    def __init__(
        self,
        api_hash: str | None = None,
        url: str | None = None,
        version: str | None = None,
        raise_for_status: bool = True,
        timeout: float | tuple[float, float] | None = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Inicializa el cliente API con la configuración de las solicitudes.

        :param str api_hash: Hash de autenticación del usuario. Si es None, se
            intentará obtener de la variable de entorno LIBREDTE_HASH.
        :param str url: URL base del servicio de LibreDTE. Si es None, se
            intentará obtener de la variable de entorno LIBREDTE_URL o se
            usará la URL por defecto.
        :param str version: Versión de la API a utilizar. Por defecto, se
            usa una versión predefinida.
        :param bool raise_for_status: Si se debe lanzar una excepción
            automáticamente para respuestas de error HTTP (y redirecciones).
            Por defecto es True.
        :param timeout: Tiempo máximo de espera de las solicitudes, en
            segundos: un número, o una tupla (conexión, respuesta). Por
            defecto es :attr:`DEFAULT_TIMEOUT`; None espera sin límite.
        :type timeout: float, tuple, optional
        :raises ApiException: Si el hash del usuario no es válido o está
            ausente.
        """
        self.set_hash(api_hash)
        self.url = self.__validate_url(url)
        self.headers = self.__generate_headers()
        self.version = version or self.__DEFAULT_VERSION
        self.raise_for_status = raise_for_status
        self.timeout = timeout
        self.session = self.__create_session()
        self.set_ssl()
        self.set_contribuyente()
        self.set_ambiente_sii()

    def __create_session(self) -> requests.Session:
        """
        Crea la sesión HTTP con que se hacen las solicitudes a la API.

        La sesión reutiliza las conexiones al servidor. Si no logra
        conectarse, reintenta hasta :attr:`CONNECT_RETRIES` veces (esperando
        0, 1 y 2 segundos): es seguro para cualquier solicitud, ya que no
        llegó al servidor. Si la solicitud llegó, no se reintenta, porque
        operaciones como emitir o eliminar no se deben repetir.

        La sesión no guarda cookies: cada solicitud se autentica con el hash
        y no depende de las anteriores.

        :return: Sesión HTTP configurada.
        :rtype: requests.Session
        """
        session = requests.Session()
        session.cookies.set_policy(DefaultCookiePolicy(allowed_domains=[]))
        # read y other en False: esos errores no se reintentan y se relanzan
        # tal cual (con 0, urllib3 los envolvería en MaxRetryError y un
        # timeout de lectura se informaría como error de conexión)
        reintentos = Retry(
            total=self.CONNECT_RETRIES,
            connect=self.CONNECT_RETRIES,
            read=False,
            status=0,
            other=False,
            backoff_factor=0.5,
        )
        adapter = HTTPAdapter(max_retries=reintentos)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    def __validate_hash(self, api_hash: str | None) -> str:
        """
        Valida y retorna el hash de autenticación.

        :param str api_hash: Hash de autenticación a validar.
        :return: Hash validado.
        :rtype: str
        :raises ApiException: Si el hash no es válido o está ausente.
        """
        valor = api_hash or getenv('LIBREDTE_HASH')
        if not valor:
            msg = 'Se debe configurar la variable de entorno: LIBREDTE_HASH.'
            raise ApiException(msg)
        valor = str(valor).strip()
        if len(valor) != self.__HASH_LENGTH:
            msg = (
                f'El hash del usuario debe ser de {self.__HASH_LENGTH} '
                'caracteres.'
            )
            raise ApiException(msg)
        return valor

    def __validate_url(self, url: str | None) -> str:
        """
        Valida y retorna la URL base para la API.

        Se quita la '/' final, si la tiene. Si la URL usa HTTP (sin cifrar)
        y no es de un servidor local, se emite un aviso, ya que el hash del
        usuario viajaría sin cifrar.

        :param str url: URL a validar.
        :return: URL validada.
        :rtype: str
        """
        if url:
            valor = str(url).strip()
        else:
            valor = getenv('LIBREDTE_URL', self.__DEFAULT_URL).strip()
        valor = valor.rstrip('/')
        url_parseada = urlparse(valor)
        if (
            url_parseada.scheme == 'http'
            and url_parseada.hostname not in self.__LOCAL_HOSTS
        ):
            warnings.warn(
                f'La URL {valor} no usa HTTPS: el hash del usuario viajará '
                'sin cifrar.',
                UserWarning,
                stacklevel=3,
            )
        return valor

    def __generate_headers(self) -> dict[str, str]:
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

    def set_ssl(self, ssl_check: bool = True) -> bool:
        """
        Configura las opciones de SSL para las conexiones HTTP.

        Este método permite activar o desactivar la verificación del
        certificado SSL del servidor. Si se activa, las conexiones HTTP
        verificarán el certificado SSL del servidor; si se desactiva, no lo
        harán.

        :param bool ssl_check: Indica si se debe verificar el certificado SSL
            del host. Por defecto es True.

        :return: El estado actualizado de la verificación del SSL.
        :rtype: bool

        Ejemplo de uso:
        client.set_ssl(False)  # Desactiva la verificación SSL
        """
        self.ssl_check = ssl_check
        return self.ssl_check

    def set_contribuyente(self, rut: int | str | None = None) -> int | None:
        """
        Establece el RUT del contribuyente para las solicitudes de la API.

        Este método permite configurar el RUT del contribuyente que se
        utilizará en las solicitudes subsiguientes. Si se proporciona un RUT,
        este se utiliza; de lo contrario, se intenta obtener de la variable
        de entorno 'LIBREDTE_RUT'.

        :param rut: RUT del contribuyente a establecer, con o sin dígito
            verificador. Si es None, se intentará obtener de la variable de
            entorno 'LIBREDTE_RUT'. Si es '', se quita el contribuyente.
        :type rut: int, str, optional
        :return: El RUT del contribuyente configurado, o None si no hay.
        :rtype: int
        :raises ApiException: Si el RUT es inválido o no se puede convertir a
            entero.
        """
        valor = rut if rut is not None else getenv('LIBREDTE_RUT')
        if isinstance(valor, str):
            valor = valor.strip()
        if valor is None or valor == '':
            self.rut = None
            return self.rut
        valor = _rut_sin_dv(valor)
        try:
            self.rut = int(valor)
        except ValueError as error:
            msg = f'Valor de RUT inválido: {valor}'
            raise ApiException(msg) from error
        return self.rut

    def set_hash(self, api_hash: str | None) -> None:
        """
        Configura la autenticación HTTP básica usando un hash proporcionado.

        Este método toma un hash, lo valida (o transforma) en un nombre de
        usuario mediante `__validate_hash` y establece la autenticación HTTP
        básica para su uso en futuras solicitudes HTTP. La contraseña se
        establece como un valor predeterminado 'X'.

        :param str api_hash: Un hash que se valida y se usa para configurar el
            nombre de usuario en la autenticación HTTP básica.
        """
        username = self.__validate_hash(api_hash)
        password = 'X'
        self.http_auth = HTTPBasicAuth(username, password)

    def set_ambiente_sii(
        self,
        ambiente: int | str | None = None,
    ) -> int | None:
        """
        Establece el ambiente del SII para las solicitudes de la API.

        Este método permite configurar el ambiente del Servicio de Impuestos
        Internos (SII), producción o pruebas, que se utilizará en las
        solicitudes subsiguientes. El ambiente se puede especificar
        directamente o ser obtenido de la variable de entorno
        'LIBREDTE_AMBIENTE'. Los valores válidos son identificadores para
        producción ('0', 'produccion', 'prod', 'palena') y pruebas ('1',
        'pruebas', 'test', 'maullin'), sin distinguir mayúsculas.

        :param ambiente: Identificador del ambiente a establecer. Si es
            None, se intentará obtener de la variable de entorno
            'LIBREDTE_AMBIENTE'.
        :type ambiente: int, str, optional
        :return: El ambiente del SII configurado
            (:attr:`AMBIENTE_SII_PRODUCCION` o :attr:`AMBIENTE_SII_PRUEBAS`),
            o None si no se configuró.
        :rtype: int
        :raises ApiException: Si el valor proporcionado para el ambiente es
            inválido.
        """
        valor = ambiente if ambiente is not None else getenv(
            'LIBREDTE_AMBIENTE',
        )
        self.ambiente_sii = None
        if valor is not None and valor != '':
            texto = str(valor).strip()
            clave = texto.lower()
            if clave in ('0', 'produccion', 'prod', 'palena'):
                self.ambiente_sii = self.AMBIENTE_SII_PRODUCCION
            elif clave in ('1', 'pruebas', 'test', 'maullin'):
                self.ambiente_sii = self.AMBIENTE_SII_PRUEBAS
            else:
                msg = f'Valor de Ambiente SII inválido: {texto}'
                raise ApiException(msg)
        return self.ambiente_sii

    def get(
        self,
        resource: str,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """
        Realiza una solicitud GET a un recurso de la API de LibreDTE.

        :param str resource: Recurso de la API que se desea consumir.
        :param dict headers: Cabeceras adicionales para la solicitud. Si es
            None, se usarán las cabeceras por defecto.
        :return: Objeto de respuesta de la solicitud HTTP.
        :rtype: requests.Response
        :raises ApiException: Lanza una excepción si ocurre un error en la
            solicitud HTTP, como errores de conexión, timeout o HTTP.
        """
        return self.__request('GET', resource, headers=headers)

    def post(
        self,
        resource: str,
        data: Mapping[str, object] | Sequence[object] | str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """
        Realiza una solicitud POST a un recurso de la API de LibreDTE.

        :param str resource: Recurso de la API que se desea consumir.
        :param dict, str data: Datos que se enviarán con la solicitud. Si es
            un diccionario, se codificará como JSON.
        :param dict headers: Cabeceras adicionales para la solicitud. Si es
            None, se usarán las cabeceras por defecto.
        :return: Objeto de respuesta de la solicitud HTTP.
        :rtype: requests.Response
        :raises ApiException: Lanza una excepción si ocurre un error en la
            solicitud HTTP, como errores de conexión, timeout o HTTP.
        """
        return self.__request('POST', resource, data, headers)

    def __request(
        self,
        method: Literal['GET', 'POST'],
        resource: str,
        data: Mapping[str, object] | Sequence[object] | str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud
            (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si los datos no se pueden codificar en JSON o
            si hay un error de conexión, timeout o HTTP.
        """
        api_path = f'/api/{resource}'
        full_url = urljoin(self.url + '/', api_path.lstrip('/'))
        extra_params: dict[str, str | int] = {'_version': self.version}
        if self.rut is not None:
            extra_params['_contribuyente_rut'] = self.rut
        if self.ambiente_sii is not None:
            extra_params['_contribuyente_certificacion'] = self.ambiente_sii
        full_url = self.__add_parameters_to_url(full_url, extra_params)
        request_headers = {**self.headers, **(headers or {})}
        body: str | None
        if data is None:
            body = None
        elif isinstance(data, str):
            body = data
        else:
            try:
                body = json.dumps(data)
            except (TypeError, ValueError) as error:
                # TypeError: tipo no serializable; ValueError: referencia
                # circular o un valor no válido en JSON.
                msg = f'Error al codificar los datos en JSON: {error}'
                raise ApiException(msg) from error
        try:
            response = self.session.request(
                method,
                full_url,
                data=body,
                headers=request_headers,
                auth=self.http_auth,
                verify=self.ssl_check,
                timeout=self.timeout,
                # Una redirección convertiría un POST en GET y perdería sus
                # datos: se informa como error (ver
                # __check_and_return_response)
                allow_redirects=False,
            )
        # Timeout va antes que ConnectionError: ConnectTimeout hereda de ambas
        # y es un timeout.
        except requests.exceptions.Timeout as error:
            msg = f'Error de timeout: {error}'
            raise ApiException(msg) from error
        except requests.exceptions.ConnectionError as error:
            msg = f'Error de conexión: {error}'
            raise ApiException(msg) from error
        except requests.exceptions.RequestException as error:
            msg = f'Error en la solicitud: {error}'
            raise ApiException(msg) from error
        return self.__check_and_return_response(response)

    def __add_parameters_to_url(
        self,
        url: str,
        params: Mapping[str, str | int],
    ) -> str:
        """
        Añade o actualiza parámetros en la URL dada.

        Esta función toma una URL y un diccionario de parámetros, y devuelve
        una nueva URL con los parámetros añadidos o actualizados. Si un
        parámetro ya existe en la URL, su valor se actualizará; si no existe,
        el parámetro se añadirá.

        :param str url: La URL original a la que se añadirán los parámetros.
        :param dict params: Un diccionario de parámetros y valores para
            añadir a la URL.
        :return: La URL con los parámetros añadidos o actualizados.
        :rtype: str
        """
        # Descomponer la URL en sus componentes
        parsed_url = urlparse(url)

        # Extraer y modificar los parámetros de query
        query_params: dict[str, list[str] | str | int] = {
            # keep_blank_values: los filtros con valor vacío se mantienen
            **parse_qs(parsed_url.query, keep_blank_values=True),
            **params,
        }

        # Reconstruir la query string
        new_query_string = urlencode(query_params, doseq=True)

        # Reconstruir la URL completa
        return urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query_string,
                parsed_url.fragment,
            ),
        )

    def __check_and_return_response(
        self,
        response: requests.Response,
    ) -> requests.Response:
        """
        Verifica la respuesta de la solicitud HTTP y maneja los errores.

        :param requests.Response response: Objeto de respuesta de requests.
        :return: Respuesta validada.
        :rtype: requests.Response
        :raises ApiException: Si la respuesta contiene un error HTTP o una
            redirección.
        """
        if (
            self.raise_for_status
            and HTTPStatus.MULTIPLE_CHOICES
            <= response.status_code
            < HTTPStatus.BAD_REQUEST
        ):
            location = response.headers.get('Location', '')
            msg = (
                f'La API respondió con una redirección a "{location}". '
                'Revise la URL configurada (LIBREDTE_URL), por ejemplo si '
                'debe usar https.'
            )
            raise ApiException(msg, response.status_code)
        if response.status_code != HTTPStatus.OK and self.raise_for_status:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                message, params = self.__get_error(response)
                raise ApiException(
                    message,
                    response.status_code,
                    params,
                ) from error
        return response

    def __get_error(
        self,
        response: requests.Response,
    ) -> tuple[str, dict[str, object] | None]:
        """
        Obtiene el mensaje y los datos de una respuesta HTTP con error.

        El mensaje es el cuerpo de la respuesta si es un texto JSON, o su
        campo 'message' si es un objeto JSON. Si es un objeto JSON, también
        se entrega completo, como parámetros del error.

        :param requests.Response response: Respuesta HTTP con error.
        :return: Mensaje de error y objeto JSON de la respuesta (o None).
        :rtype: tuple
        """
        try:
            body: object = response.json()
        except requests.exceptions.JSONDecodeError:
            return (
                f'Error al decodificar los datos en JSON: {response.text}',
                None,
            )
        if isinstance(body, str):
            return body, None
        if _is_dict(body):
            return str(body.get('message', 'Error desconocido.')), body
        return 'Error desconocido.', None

    def create_link(
        self,
        resource: str | None,
        rut: int | str | None = None,
    ) -> str:
        """
        Crea un enlace a un recurso específico en la plataforma de LibreDTE.

        :param str resource: Recurso al que se desea acceder en la plataforma
            de LibreDTE.
        :param int rut: RUT del contribuyente en LibreDTE con el que se
            quiere usar el recurso. Si es None, se usará el RUT almacenado en
            la clase.
        :return: URL formada para acceder al recurso especificado.
        :rtype: str
        :raises ApiException: Si el RUT es inválido o está ausente.

        .. note::
            Si el recurso codificado en base64 contiene '/', LibreDTE lo
            recibe truncado: su router separa la ruta por '/' antes de
            decodificarla.
        """
        valor = rut or self.rut
        msg = f'Valor de RUT inválido: {valor}'
        if valor is None:
            raise ApiException(msg)
        try:
            rut_numero = int(_rut_sin_dv(valor))
        except ValueError as error:
            raise ApiException(msg) from error
        link = f'{self.url}/dte/contribuyentes/seleccionar/{rut_numero}'
        if resource:
            resource_base64 = base64.b64encode(
                resource.encode('utf-8'),
            ).decode('utf-8')
            # '+' se escapa: el servidor lo decodificaría como espacio
            link = f'{link}/{quote(resource_base64, safe="")}'
        return link


def _rut_sin_dv(rut: int | str) -> int | str:
    """
    Quita los puntos y el dígito verificador de un RUT en texto con DV.

    :param rut: RUT, por ejemplo 76192083 o '76.192.083-9'.
    :type rut: int, str
    :return: RUT sin dígito verificador (sin convertir a entero).
    :rtype: int, str
    """
    if isinstance(rut, str) and '-' in rut:
        return rut.replace('.', '').split('-')[0]
    return rut


def _is_dict(value: object) -> TypeIs[dict[str, object]]:
    """
    Verifica si el valor es un diccionario (un objeto JSON).

    A diferencia de ``isinstance(value, dict)``, informa a los chequeadores
    de tipos que las llaves son textos, como en un objeto JSON.

    :param object value: Valor a verificar.
    :return: Si el valor es un diccionario.
    :rtype: bool
    """
    return isinstance(value, dict)


class ApiException(Exception):

    """
    Excepción personalizada para errores en el cliente de la API.

    :param str message: Mensaje de error.
    :param int code: Código de error (opcional).
    :param dict params: Parámetros adicionales del error (opcional). En los
        errores HTTP es el objeto JSON de la respuesta, si lo hay.
    """

    def __init__(
        self,
        message: str,
        code: int | None = None,
        params: Mapping[str, object] | None = None,
    ) -> None:
        """
        Inicializa la excepción con su mensaje, código y parámetros.

        :param str message: Mensaje de error.
        :param int code: Código de error (opcional).
        :param dict params: Parámetros adicionales del error (opcional).
        """
        self.message = message
        self.code = code
        self.params = params
        super().__init__(message)

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del error.

        La representación entrega un contexto claro del problema ocurrido:
        incluye el prefijo "[LibreDTE]", seguido del código de error si está
        presente, y el mensaje de error.

        Si se especifica un código de error, el formato será:
        "[LibreDTE] Error {code}: {message}"

        Si no se especifica un código de error, el formato será:
        "[LibreDTE] {message}"

        :return: Una cadena que representa el error de una manera clara y
            concisa.
        """
        if self.code is not None:
            return f'[LibreDTE] Error {self.code}: {self.message}'
        return f'[LibreDTE] {self.message}'


class ApiBase:

    """
    Clase base para las clases que consumen la API (wrappers).

    :param str api_hash: Hash de autenticación del usuario. Si es None, se
        intentará obtener de la variable de entorno LIBREDTE_HASH.
    :param str api_url: URL base del servicio de LibreDTE. Si es None, se
        intentará obtener de la variable de entorno LIBREDTE_URL o se usará
        la URL por defecto.
    :param str api_version: Versión de la API a utilizar. Por defecto, se usa
        una versión predefinida.
    :param bool api_raise_for_status: Si se debe lanzar una excepción
        automáticamente para respuestas de error HTTP. Por defecto es True.
    """

    def __init__(
        self,
        api_hash: str | None = None,
        api_url: str | None = None,
        api_version: str | None = None,
        api_raise_for_status: bool = True,
        api_timeout: float | tuple[float, float] | None = (
            ApiClient.DEFAULT_TIMEOUT
        ),
    ) -> None:
        """
        Inicializa el cliente de la API que usan los wrappers.

        :param str api_hash: Hash de autenticación del usuario.
        :param str api_url: URL base del servicio de LibreDTE.
        :param str api_version: Versión de la API a utilizar.
        :param bool api_raise_for_status: Si se debe lanzar una excepción
            automáticamente para respuestas de error HTTP.
        :param api_timeout: Tiempo máximo de espera de las solicitudes, en
            segundos (ver :class:`ApiClient`).
        :type api_timeout: float, tuple, optional
        """
        self.client = ApiClient(
            api_hash,
            api_url,
            api_version,
            api_raise_for_status,
            api_timeout,
        )

    @staticmethod
    def _ruta(recurso: str, *valores: str | int) -> str:
        """
        Arma la ruta de un recurso de la API, con sus valores escapados.

        Cada valor (RUT, tipo de DTE, folio, código) se escapa para que no
        cambie la ruta: por ejemplo, un '+' de un código base64 llegaría al
        servidor como espacio.

        :param str recurso: Ruta fija del recurso, por ejemplo
            '/dte/dte_emitidos/info'.
        :param valores: Valores que se agregan a la ruta.
        :return: Ruta del recurso con sus valores.
        :rtype: str
        :raises ApiException: Si un valor está vacío, es '.' o '..', o
            contiene '/', ya que llevaría la solicitud a otro recurso.
        """
        segmentos = [recurso]
        for valor in valores:
            texto = str(valor)
            if texto in ('', '.', '..') or '/' in texto:
                msg = f'Valor inválido para la URL de la API: {texto!r}'
                raise ApiException(msg)
            segmentos.append(quote(texto, safe=''))
        return '/'.join(segmentos)

    @staticmethod
    def _query(filtros: Mapping[str, object] | None) -> str:
        """
        Codifica los filtros como parámetros de la URL (query string).

        Los booleanos se envían como 1 y 0: la API (PHP) interpreta el texto
        "False" como verdadero.

        :param dict filtros: Filtros a codificar, o None.
        :return: Parámetros codificados, o '' si no hay filtros.
        :rtype: str
        """
        if filtros is None:
            return ''
        return urlencode(
            {
                nombre: int(valor) if isinstance(valor, bool) else valor
                for nombre, valor in filtros.items()
            },
        )
