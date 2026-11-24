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
Respuestas de la API que usan las pruebas, validadas al leerlas.

Cada tipo declara solo los campos que leen las pruebas. Los campos salen del
código de la API (controladores y consultas de LibreDTE), ya que el esquema
OpenAPI publicado no documenta estas respuestas.

La API entrega los enteros de la base de datos como número o como texto
(según la versión de PHP), por eso los RUT, tipos de DTE, folios y totales
se aceptan como ``int`` o ``str``: el cliente acepta ambos en las URL.

Si una respuesta no tiene la forma esperada, la prueba falla indicando qué
se recibió, en vez de fallar más adelante con un ``KeyError``.
"""

from collections.abc import Mapping
from typing import TypedDict, TypeIs

import requests

# Tipos aceptados para cada campo: entero (como número o texto) o texto.
_ENTERO: tuple[type, ...] = (int, str)
_TEXTO: tuple[type, ...] = (str,)


class DteTemporal(TypedDict):

    """DTE temporal creado (POST /dte/documentos/emitir)."""

    emisor: int | str
    receptor: int | str
    dte: int | str
    codigo: str


class DteTemporalBuscado(TypedDict):

    """
    DTE de la búsqueda de temporales (POST /dte/dte_tmps/buscar/...).

    No incluye el emisor: es el contribuyente de la búsqueda.
    """

    receptor: int | str
    dte: int | str
    codigo: str


class DteEmitido(TypedDict):

    """
    DTE de la búsqueda de emitidos (POST /dte/dte_emitidos/buscar).

    No incluye el emisor: es el contribuyente de la búsqueda.
    """

    dte: int | str
    folio: int | str
    fecha: str
    total: int | str


class DteRecibido(TypedDict):

    """
    DTE de la búsqueda de recibidos (POST /dte/dte_recibidos/buscar).

    No incluye el receptor: es el contribuyente de la búsqueda.
    """

    emisor: int | str
    dte: int | str
    folio: int | str
    fecha: str


class Cobro(TypedDict):

    """Cobro de un DTE temporal (GET /dte/dte_tmps/cobro/...)."""

    codigo: str


def _es_objeto(valor: object) -> TypeIs[dict[str, object]]:
    """Indica si el valor es un objeto JSON."""
    return isinstance(valor, dict)


def _es_lista(valor: object) -> TypeIs[list[object]]:
    """Indica si el valor es un arreglo JSON."""
    return isinstance(valor, list)


def _tiene_campos(
    valor: object,
    campos: Mapping[str, tuple[type, ...]],
) -> bool:
    """Indica si el valor es un objeto JSON con los campos y sus tipos."""
    if not _es_objeto(valor):
        return False
    return all(
        nombre in valor
        and isinstance(valor[nombre], tipos)
        and not isinstance(valor[nombre], bool)
        for nombre, tipos in campos.items()
    )


def es_dte_temporal(valor: object) -> TypeIs[DteTemporal]:
    """Indica si el valor es un DTE temporal."""
    return _tiene_campos(
        valor,
        {
            'emisor': _ENTERO,
            'receptor': _ENTERO,
            'dte': _ENTERO,
            'codigo': _TEXTO,
        },
    )


def es_dte_temporal_buscado(valor: object) -> TypeIs[DteTemporalBuscado]:
    """Indica si el valor es un DTE de la búsqueda de temporales."""
    return _tiene_campos(
        valor,
        {'receptor': _ENTERO, 'dte': _ENTERO, 'codigo': _TEXTO},
    )


def es_dte_emitido(valor: object) -> TypeIs[DteEmitido]:
    """Indica si el valor es un DTE de la búsqueda de emitidos."""
    return _tiene_campos(
        valor,
        {
            'dte': _ENTERO,
            'folio': _ENTERO,
            'fecha': _TEXTO,
            'total': _ENTERO,
        },
    )


def es_dte_recibido(valor: object) -> TypeIs[DteRecibido]:
    """Indica si el valor es un DTE de la búsqueda de recibidos."""
    return _tiene_campos(
        valor,
        {
            'emisor': _ENTERO,
            'dte': _ENTERO,
            'folio': _ENTERO,
            'fecha': _TEXTO,
        },
    )


def es_cobro(valor: object) -> TypeIs[Cobro]:
    """Indica si el valor es un cobro."""
    return _tiene_campos(valor, {'codigo': _TEXTO})


def es_lista_dte_temporales(
    valor: object,
) -> TypeIs[list[DteTemporalBuscado]]:
    """Indica si el valor es un listado de DTE temporales."""
    return _es_lista(valor) and all(
        es_dte_temporal_buscado(item) for item in valor
    )


def es_lista_dte_emitidos(valor: object) -> TypeIs[list[DteEmitido]]:
    """Indica si el valor es un listado de DTE emitidos."""
    return _es_lista(valor) and all(es_dte_emitido(item) for item in valor)


def es_lista_dte_recibidos(valor: object) -> TypeIs[list[DteRecibido]]:
    """Indica si el valor es un listado de DTE recibidos."""
    return _es_lista(valor) and all(es_dte_recibido(item) for item in valor)


def _invalida(response: requests.Response, esperado: str) -> AssertionError:
    """Error de prueba para una respuesta que no tiene la forma esperada."""
    return AssertionError(
        f'La respuesta de {response.url} no es {esperado}: {response.text}',
    )


def leer_objeto(response: requests.Response) -> dict[str, object]:
    """
    Lee una respuesta que debe ser un objeto JSON.

    :param requests.Response response: Respuesta de la API.
    :return: Objeto JSON de la respuesta.
    :raises AssertionError: Si la respuesta no es un objeto JSON.
    """
    datos: object = response.json()
    if not _es_objeto(datos):
        raise _invalida(response, 'un objeto JSON')
    return datos


def leer_dte_temporal(response: requests.Response) -> DteTemporal:
    """
    Lee la respuesta de la emisión de un DTE temporal.

    :param requests.Response response: Respuesta de la API.
    :return: DTE temporal creado.
    :raises AssertionError: Si la respuesta no es un DTE temporal.
    """
    datos: object = response.json()
    if not es_dte_temporal(datos):
        raise _invalida(response, 'un DTE temporal')
    return datos


def leer_dtes_emitidos(response: requests.Response) -> list[DteEmitido]:
    """
    Lee la respuesta de la búsqueda de DTE emitidos.

    :param requests.Response response: Respuesta de la API.
    :return: DTE emitidos encontrados.
    :raises AssertionError: Si la respuesta no es un listado de DTE
        emitidos.
    """
    datos: object = response.json()
    if not es_lista_dte_emitidos(datos):
        raise _invalida(response, 'un listado de DTE emitidos')
    return datos


def leer_dtes_recibidos(response: requests.Response) -> list[DteRecibido]:
    """
    Lee la respuesta de la búsqueda de DTE recibidos.

    :param requests.Response response: Respuesta de la API.
    :return: DTE recibidos encontrados.
    :raises AssertionError: Si la respuesta no es un listado de DTE
        recibidos.
    """
    datos: object = response.json()
    if not es_lista_dte_recibidos(datos):
        raise _invalida(response, 'un listado de DTE recibidos')
    return datos


def leer_cobro(response: requests.Response) -> Cobro:
    """
    Lee la respuesta del cobro de un DTE temporal.

    :param requests.Response response: Respuesta de la API.
    :return: Cobro del DTE temporal.
    :raises AssertionError: Si la respuesta no es un cobro.
    """
    datos: object = response.json()
    if not es_cobro(datos):
        raise _invalida(response, 'un cobro')
    return datos


def leer_lista_objetos(response: requests.Response) -> list[dict[str, object]]:
    """
    Lee una respuesta que debe ser un arreglo JSON de objetos.

    :param requests.Response response: Respuesta de la API.
    :return: Objetos del arreglo JSON.
    :raises AssertionError: Si la respuesta no es un arreglo de objetos.
    """
    datos: object = response.json()
    if not _es_lista(datos):
        raise _invalida(response, 'un arreglo JSON')
    objetos: list[dict[str, object]] = []
    for item in datos:
        if not _es_objeto(item):
            raise _invalida(response, 'un arreglo de objetos JSON')
        objetos.append(item)
    return objetos


def leer_texto(response: requests.Response) -> str:
    """
    Lee una respuesta que debe ser un texto JSON (ej. un XML en base64).

    :param requests.Response response: Respuesta de la API.
    :return: Texto de la respuesta.
    :raises AssertionError: Si la respuesta no es un texto JSON.
    """
    datos: object = response.json()
    if not isinstance(datos, str):
        raise _invalida(response, 'un texto JSON')
    return datos


def leer_booleano(response: requests.Response) -> bool:
    """
    Lee una respuesta que debe ser un booleano JSON.

    :param requests.Response response: Respuesta de la API.
    :return: Booleano de la respuesta.
    :raises AssertionError: Si la respuesta no es un booleano JSON.
    """
    datos: object = response.json()
    if not isinstance(datos, bool):
        raise _invalida(response, 'un booleano JSON')
    return datos


def leer_dte_emitido(response: requests.Response) -> DteEmitido:
    """
    Lee una respuesta que debe ser un DTE emitido (real).

    :param requests.Response response: Respuesta de la API.
    :return: DTE emitido.
    :raises AssertionError: Si la respuesta no es un DTE emitido.
    """
    datos: object = response.json()
    if not es_dte_emitido(datos):
        raise _invalida(response, 'un DTE emitido')
    return datos


def leer_dte_recibido(response: requests.Response) -> DteRecibido:
    """
    Lee una respuesta que debe ser un DTE recibido.

    :param requests.Response response: Respuesta de la API.
    :return: DTE recibido.
    :raises AssertionError: Si la respuesta no es un DTE recibido.
    """
    datos: object = response.json()
    if not es_dte_recibido(datos):
        raise _invalida(response, 'un DTE recibido')
    return datos


def leer_dtes_temporales(
    response: requests.Response,
) -> list[DteTemporalBuscado]:
    """
    Lee la respuesta de la búsqueda de DTE temporales.

    :param requests.Response response: Respuesta de la API.
    :return: DTE temporales encontrados.
    :raises AssertionError: Si la respuesta no es un listado de DTE
        temporales.
    """
    datos: object = response.json()
    if not es_lista_dte_temporales(datos):
        raise _invalida(response, 'un listado de DTE temporales')
    return datos
