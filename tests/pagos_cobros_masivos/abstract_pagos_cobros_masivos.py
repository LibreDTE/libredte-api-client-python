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

"""Clase base de las pruebas de pagos y cobros masivos."""

from datetime import datetime, timedelta
from typing import ClassVar

import requests

from libredte.api_client import ApiClient
from libredte.api_client.cobros import Cobros
from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)


class AbstractPagosCobrosMasivos(AbstractDteFacturacion):

    """
    Clase heredable para pagos y cobros masivos.

    Hereda la preparación del cliente de DTE y la emisión de DTE temporales
    (que se eliminan al terminar cada prueba, junto a su cobro si no está
    pagado).
    """

    cobros: ClassVar[Cobros]

    @classmethod
    def setUpClass(cls) -> None:
        """Prepara los clientes de DTE y de cobros de la API."""
        super().setUpClass()
        cls.cobros = Cobros()
        cls.cobros.client.set_contribuyente(cls.contribuyente_rut)
        cls.cobros.client.set_ambiente_sii(ApiClient.AMBIENTE_SII_PRUEBAS)

    def _buscar_cobro_dte_temp(self, rut: str) -> requests.Response:
        """
        Busca el cobro de un DTE temporal emitido para la prueba.

        :param str rut: RUT del emisor asociado al cobro.
        :return: Respuesta JSON con el cobro del DTE temporal.
        """
        dte_temporal = self._emitir_dte_temporal(self.datos)
        return self.cobros.get_cobro_dte_temporal(
            dte_temporal['receptor'],
            dte_temporal['dte'],
            dte_temporal['codigo'],
            rut,
        )

    def _listar_cobros(self, rut: str) -> requests.Response:
        """
        Método heredable para listar cobros.

        :param str rut: RUT del emisor del cobro.
        :return: Respuesta JSON con el listado de cobros.
        """
        hoy = datetime.now().astimezone()
        filtros = {
            'fecha_desde': (hoy - timedelta(days=30)).strftime('%Y-%m-%d'),
            'fecha_hasta': hoy.strftime('%Y-%m-%d'),
            'pagado': False,
        }
        return self.cobros.get_cobros(rut, filtros)
