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

"""Clase base de las pruebas de facturación de DTE."""

import json
import unittest
from collections.abc import Mapping
from datetime import datetime, timedelta
from http import HTTPStatus
from os import getenv
from typing import ClassVar

import requests

from libredte.api_client import ApiClient, ApiException
from libredte.api_client.dte import Dte
from tests.datos import datos_dte_temporal
from tests.respuestas import (
    DteEmitido,
    DteRecibido,
    DteTemporal,
    leer_dte_temporal,
    leer_dtes_emitidos,
    leer_dtes_recibidos,
)


class AbstractDteFacturacion(unittest.TestCase):

    """
    Clase heredable para manejar facturación de DTEs.

    Las pruebas usan la API real con el contribuyente de LIBREDTE_RUT, en el
    ambiente de pruebas del SII. Los DTE temporales que emiten se eliminan
    al terminar cada prueba.
    """

    # Se asignan al preparar cada clase de pruebas (setUpClass).
    dte: ClassVar[Dte]
    verbose: ClassVar[bool]
    contribuyente_rut: ClassVar[str]
    # Filtros para los listados: documentos de los últimos 30 días.
    filtros: ClassVar[dict[str, str]]
    # Datos del DTE que emiten las pruebas.
    datos: ClassVar[dict[str, object]]

    @classmethod
    def setUpClass(cls) -> None:
        """Prepara el cliente de la API para el contribuyente de prueba."""
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.contribuyente_rut = getenv('LIBREDTE_RUT', '').strip()
        if not cls.contribuyente_rut:
            msg = 'Se debe configurar la variable de entorno LIBREDTE_RUT.'
            raise RuntimeError(msg)
        # Un cliente por clase de pruebas: la configuración de una clase no
        # afecta a las demás.
        cls.dte = Dte()
        cls.dte.client.set_contribuyente(cls.contribuyente_rut)
        cls.dte.client.set_ambiente_sii(ApiClient.AMBIENTE_SII_PRUEBAS)
        hoy = datetime.now().astimezone()
        cls.filtros = {
            'fecha_desde': (hoy - timedelta(days=30)).strftime('%Y-%m-%d'),
            'fecha_hasta': hoy.strftime('%Y-%m-%d'),
        }
        cls.datos = datos_dte_temporal(cls.contribuyente_rut)

    def _mostrar(self, etiqueta: str, valor: object) -> None:
        """
        Muestra un resultado en pantalla, si TEST_VERBOSE es 1.

        :param str etiqueta: Descripción del resultado.
        :param object valor: Resultado (texto, o datos que se muestran como
            JSON).
        """
        if self.verbose:
            texto = valor if isinstance(valor, str) else json.dumps(valor)
            print(f'{self.id()} {etiqueta}:', texto)

    def _listar_dtes_temp(self, rut: str) -> requests.Response:
        """
        Método heredable para buscar y listar DTEs temporales.

        :param str rut: RUT del emisor asociado a los DTEs temporales.
        :return: Respuesta JSON con la lista de DTEs temporales.
        """
        return self.dte.get_dte_temporales(rut, self.filtros)

    def _listar_dtes_reales(self, rut: str) -> requests.Response:
        """
        Método heredable para buscar y listar DTEs reales.

        :param str rut: RUT del emisor asociado a los DTEs reales.
        :return: Respuesta JSON con la lista de DTEs reales.
        """
        return self.dte.get_dte_emitidos(rut, self.filtros)

    def _listar_dtes_recibidos(self, rut: str) -> requests.Response:
        """
        Método heredable para buscar y listar DTEs recibidos.

        :param str rut: RUT del emisor asociado a los DTEs recibidos.
        :return: Respuesta JSON con la lista de DTEs recibidos.
        """
        return self.dte.get_dte_recibidos(rut, self.filtros)

    def _emitir_dte_temporal(
        self,
        datos: Mapping[str, object],
    ) -> DteTemporal:
        """
        Realiza la emisión de un DTE temporal, que se elimina al terminar.

        :param dict datos: Datos del DTE temporal a emitir.
        :return: DTE temporal emitido.
        """
        dte_temporal = leer_dte_temporal(self.dte.emitir_dte_temporal(datos))
        self.addCleanup(self._eliminar_dte_temporal, dte_temporal)
        return dte_temporal

    def _eliminar_dte_temporal(self, dte_temporal: DteTemporal) -> None:
        """
        Elimina un DTE temporal emitido por la prueba, si aún existe.

        Si ya no existe (la prueba lo eliminó o generó el DTE real con él),
        la API responde 404 y no hay nada que eliminar.

        :param dict dte_temporal: DTE temporal a eliminar.
        """
        try:
            self.dte.delete_dte_temporal(
                dte_temporal['receptor'],
                dte_temporal['dte'],
                dte_temporal['codigo'],
                dte_temporal['emisor'],
            )
        except ApiException as e:
            if e.code != HTTPStatus.NOT_FOUND:
                raise

    def _primer_dte_emitido(self) -> DteEmitido:
        """
        Obtiene el DTE real más reciente de los últimos 30 días.

        Si no hay, la prueba se salta: depende de que existan DTE emitidos.

        :return: DTE emitido.
        """
        try:
            documentos = leer_dtes_emitidos(
                self._listar_dtes_reales(self.contribuyente_rut),
            )
        except ApiException as e:
            # La API responde 404 si la búsqueda no encuentra documentos.
            if e.code != HTTPStatus.NOT_FOUND:
                raise
            documentos = []
        if not documentos:
            self.skipTest('No hay DTE emitidos en los últimos 30 días.')
        return documentos[0]

    def _primer_dte_recibido(self) -> DteRecibido:
        """
        Obtiene el DTE recibido más reciente de los últimos 30 días.

        Si no hay, la prueba se salta: depende de que existan DTE recibidos.

        :return: DTE recibido.
        """
        documentos = leer_dtes_recibidos(
            self._listar_dtes_recibidos(self.contribuyente_rut),
        )
        if not documentos:
            self.skipTest('No hay DTE recibidos en los últimos 30 días.')
        return documentos[0]
