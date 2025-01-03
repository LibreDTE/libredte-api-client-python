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

from libredte.api_client.cobros import Cobros
from libredte.api_client.dte import Dte

from datetime import datetime, timedelta

import unittest

class AbstractPagosCobrosMasivos(unittest.TestCase):
    """
    Clase heredable para pagos y cobros masivos.
    """

    cobros = Cobros()
    dte = Dte()

    def _buscar_cobro_dte_temp(self, rut, datos):
        """
        Método heredable para buscar un cobro asociado a un DTE temporal.

        :param str rut: RUT del emisor asociado al cobro.
        :param dict datos: Datos del DTE temporal a generar.
        :return: Respuesta JSON con el cobro buscado.
        """
        dte_temp = self.__emitir_dte_temporal(datos)
        dte_dict = dte_temp.json()
        cobro = self.cobros.get_cobro_dte_temporal(
            dte_dict['receptor'],
            dte_dict['dte'],
            dte_dict['codigo'],
            rut
        )

        return cobro

    def _listar_cobros(self, rut):
        """
        Método heredable para listar cobros.

        :param str rut: RUT del emisor del cobro.
        :return: Respuesta JSON con el listado de cobros.
        """
        filtros = {
            'fecha_desde': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'fecha_hasta': datetime.now().strftime('%Y-%m-%d'),
            'pagado': False
        }

        lista_cobros = self.cobros.get_cobros(
            rut,
            filtros
        )

        return lista_cobros

    def __emitir_dte_temporal(self, datos):
        """
        Método privado para emitir un DTE temporal.

        :param dict datos: Datos del DTE temporal a generar.
        :return: Respuesta JSON con el DTE temporal generado.
        """
        dte_temporal = self.dte.emitir_dte_temporal(datos)

        return dte_temporal
