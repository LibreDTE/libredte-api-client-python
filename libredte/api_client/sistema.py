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

from . import ApiBase

class Moneda(ApiBase):
    """
    Clase para interactuar con los endpoints de moneda de la API.

    Proporciona métodos para realizar operaciones relacionadas con monedas,
    como obtener tasas de cambio de moneda para fechas específicas.
    """

    def get_moneda_cambios(self, to, day):
        """
        Obtiene la tasa de cambio de moneda de USD a otra moneda en una fecha específica.

        Este método realiza una solicitud GET para obtener la tasa de cambio desde USD
        hacia la moneda especificada por el usuario para una fecha dada. Es útil para
        consultas de conversiones de moneda históricas o actuales.

        :param str to: Código de la moneda destino a la cual se desea convertir USD.
        :param str day: Fecha de la consulta de la tasa de cambio.
        :return: Respuesta JSON con la tasa de cambio desde USD a la moneda especificada en la fecha indicada.
        """
        return self.client.get(f'/sistema/general/moneda_cambios/tasa/USD/{to}/{day}')
