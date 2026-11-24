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

"""Wrapper de los recursos de cobros de la API de LibreDTE."""

from collections.abc import Mapping

import requests

from . import ApiBase


class Cobros(ApiBase):

    """
    Clase para interactuar con los endpoints de cobros de la API.

    Proporciona métodos para realizar operaciones relacionadas con cobros,
    como obtener información sobre cobros específicos y realizar pagos de
    cobros.
    """

    def get_cobros(
        self,
        emisor: str | int,
        filtros: Mapping[str, object],
    ) -> requests.Response:
        """
        Obtiene la información de varios cobros.

        Realiza una solicitud POST para buscar información sobre múltiples
        cobros dado el identificador del emisor y filtros de los cobros.

        :param str emisor: Identificador del emisor de los cobros.
        :param dict filtros: Datos de filtrado de cobros.
        :return: Respuesta JSON con la información del cobro.
        """
        url = self._ruta('/pagos/cobros/buscar', emisor)
        return self.client.post(url, data=filtros)

    def pagar_cobro(
        self,
        codigo: str,
        emisor: str | int,
        pagar_cobro: Mapping[str, object],
    ) -> requests.Response:
        """
        Realiza el pago de un cobro.

        Envía una solicitud POST para efectuar el pago de un cobro
        específico, identificado por su código y el emisor, utilizando los
        datos proporcionados para el pago.

        :param str codigo: Código que identifica el cobro a pagar.
        :param str emisor: Identificador del emisor del cobro.
        :param dict pagar_cobro: Datos del pago a realizar.
        :return: Respuesta JSON del resultado del pago del cobro.
        """
        url = self._ruta('/pagos/cobros/pagar', codigo, emisor)
        return self.client.post(url, data=pagar_cobro)

    def get_cobro_dte_temporal(
        self,
        receptor: str | int,
        dte: str | int,
        codigo: str,
        emisor: str | int,
    ) -> requests.Response:
        """
        Obtiene la información de cobro asociada a un DTE temporal.

        Realiza una solicitud GET para buscar información de cobro basada
        en un DTE temporal, dado el RUT del receptor, el tipo de DTE, el
        código del DTE temporal, y el RUT del emisor.

        :param str receptor: RUT del receptor asociado al DTE temporal.
        :param str dte: Tipo de DTE temporal.
        :param str codigo: Código único del DTE temporal.
        :param str emisor: RUT del emisor del DTE temporal.
        :return: Respuesta JSON con la información de cobro del DTE temporal.
        """
        url = self._ruta('/dte/dte_tmps/cobro', receptor, dte, codigo, emisor)
        return self.client.get(url)

    def get_cobro_dte_real(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
    ) -> requests.Response:
        """
        Obtiene la información de cobro asociada a un DTE real específico.

        Envía una solicitud GET para buscar información de cobro basada en
        un DTE real, dado el tipo de DTE, el folio del DTE, y el RUT del
        emisor.

        :param str dte: Tipo de DTE real.
        :param str folio: Folio del DTE real.
        :param str emisor: RUT del emisor del DTE real.
        :return: Respuesta JSON con la información de cobro del DTE real.
        """
        url = self._ruta('/dte/dte_emitidos/cobro', dte, folio, emisor)
        return self.client.get(url)

    def get_cobro_info(
        self,
        codigo: str,
        emisor: str | int,
    ) -> requests.Response:
        """
        Obtiene información detallada de un cobro específico.

        Realiza una solicitud GET para recuperar detalles completos sobre un
        cobro, identificado por su código y el RUT del emisor. Esta
        información puede incluir detalles del estado del cobro, montos,
        fechas relevantes, entre otros datos específicos del cobro
        consultado.

        :param str codigo: Código único que identifica el cobro.
        :param str emisor: RUT del emisor asociado al cobro.
        :return: Respuesta JSON con la información detallada del cobro.
        """
        url = self._ruta('/pagos/cobros/info', codigo, emisor)
        return self.client.get(url)
