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

from libredte.api_client.dte import Dte

from datetime import datetime, timedelta

import unittest

class AbstractDteFacturacion(unittest.TestCase):
    """
    Clase heredable para manejar facturación de DTEs.
    """

    dte = Dte()
    # Filtros para el listado de DTEs temporales.
    filtros = {
        'fecha_desde': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'fecha_hasta': datetime.now().strftime('%Y-%m-%d'),
    }

    def _listar_dtes_temp(self, rut):
        """
        Método heredable para buscar y listar DTEs temporales.

        :param str rut: RUT del emisor asociado a los DTEs temporales.
        :return: Respuesta JSON con la lista de DTEs temporales.
        """

        # Response obtenido a partir del RUT de emisor y filtros previamente definidos.
        response = self.dte.get_dte_temporales(
            rut,
            self.filtros
        )

        return response

    def _listar_dtes_reales(self, rut):
        """
        Método heredable para buscar y listar DTEs reales.

        :param str rut: RUT del emisor asociado a los DTEs reales.
        :return: Respuesta JSON con la lista de DTEs reales.
        """

        # Response obtenido a partir del RUT de emisor y filtros previamente definidos.
        response = self.dte.get_dte_emitidos(
            rut,
            self.filtros
        )

        return response

    def _listar_dtes_recibidos(self, rut):
        """
        Método heredable para buscar y listar DTEs recibidos.

        :param str rut: RUT del emisor asociado a los DTEs recibidos.
        :return: Respuesta JSON con la lista de DTEs recibidos.
        """
        # Response obtenido a partir del RUT de emisor y filtros previamente definidos.
        response = self.dte.get_dte_recibidos(
            rut,
            self.filtros
        )

        return response

    def _emitir_dte_temporal(self, datos):
        """
        Método heredable para emitir un DTE temporal.

        :param dict datos: Datos del DTE temporal a generar.
        :return: Respuesta JSON con el DTE temporal generado.
        """
        # Response obtenido a partir de datos para un DTE temporal.
        dte_temporal = self.dte.emitir_dte_temporal(datos)

        return dte_temporal