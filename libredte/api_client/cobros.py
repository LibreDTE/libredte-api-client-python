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

class Cobros(ApiBase):
    """
    Clase para interactuar con los endpoints de cobros de la API.

    Proporciona métodos para realizar operaciones relacionadas con cobros,
    como obtener información sobre cobros específicos y realizar pagos de cobros.
    """

    def get_cobro(self, emisor, cobro):
        """
        Obtiene la información de un cobro específico.

        Realiza una solicitud POST para buscar información sobre un cobro dado
        el identificador del emisor y los datos del cobro.

        :param str emisor: Identificador del emisor del cobro.
        :param dict cobro: Datos del cobro a buscar.
        :return: Respuesta JSON con la información del cobro.
        """
        return self.client.post(f'/pagos/cobros/buscar/{emisor}', data=cobro)

    def pagar_cobro(self, codigo, emisor, pagar_cobro):
        """
        Realiza el pago de un cobro.

        Envía una solicitud POST para efectuar el pago de un cobro específico,
        identificado por su código y el emisor, utilizando los datos proporcionados
        para el pago.

        :param str codigo: Código que identifica el cobro a pagar.
        :param str emisor: Identificador del emisor del cobro.
        :param dict pagar_cobro: Datos del pago a realizar.
        :return: Respuesta JSON del resultado del pago del cobro.
        """
        return self.client.post(f'/pagos/cobros/pagar/{codigo}/{emisor}', data=pagar_cobro)
