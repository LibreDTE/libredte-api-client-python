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

    def get_cobros(self, emisor, filtros):
        """
        Obtiene la información de varios cobros.

        Realiza una solicitud POST para buscar información sobre múltiples cobros
        dado el identificador del emisor y filtros de los cobros.

        :param str emisor: Identificador del emisor de los cobros.
        :param dict filtros: Datos de filtrado de cobros.
        :return: Respuesta JSON con la información del cobro.
        """
        url = "/pagos/cobros/buscar/%(emisor)s" % {'emisor' : emisor}
        return self.client.post(url, data = filtros)

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
        url = "/pagos/cobros/pagar/%(codigo)s/%(emisor)s" % {
            'codigo' : codigo,
            'emisor' : emisor
        }
        return self.client.post(url, data = pagar_cobro)

    def get_cobro_dte_temporal(self, receptor, dte, codigo, emisor):
        """
        Obtiene la información de cobro asociada a un DTE temporal específico.

        Realiza una solicitud POST para buscar información de cobro basada en un
        DTE temporal, dado el RUT del receptor, el tipo de DTE, el código del
        DTE temporal, y el RUT del emisor.

        :param str receptor: RUT del receptor asociado al DTE temporal.
        :param str dte: Tipo de DTE temporal.
        :param str codigo: Código único del DTE temporal.
        :param str emisor: RUT del emisor del DTE temporal.
        :return: Respuesta JSON con la información de cobro del DTE temporal.
        """
        url = "/dte/dte_tmps/cobro/%(receptor)s/%(dte)s/%(codigo)s/%(emisor)s" % {
            'receptor' : receptor,
            'dte' : dte,
            'codigo' : codigo,
            'emisor' : emisor
        }
        return self.client.get(url)

    def get_cobro_dte_real(self, dte, folio, emisor):
        """
        Obtiene la información de cobro asociada a un DTE real específico.

        Envia una solicitud POST para buscar información de cobro basada en un
        DTE real, dado el tipo de DTE, el folio del DTE, y el RUT del emisor.

        :param str dte: Tipo de DTE real.
        :param str folio: Folio del DTE real.
        :param str emisor: RUT del emisor del DTE real.
        :return: Respuesta JSON con la información de cobro del DTE real.
        """
        url = "/dte/dte_emitidos/cobro/%(dte)s/%(folio)s/%(emisor)s" % {
            'dte' : dte,
            'folio' : folio,
            'emisor' : emisor
        }
        return self.client.get(url)

    def get_cobro_info(self, codigo, emisor):
        """
        Obtiene información detallada de un cobro específico.

        Realiza una solicitud POST para recuperar detalles completos sobre un
        cobro, identificado por su código y el RUT del emisor. Esta información
        puede incluir detalles del estado del cobro, montos, fechas relevantes,
        entre otros datos específicos del cobro consultado.

        :param str codigo: Código único que identifica el cobro.
        :param str emisor: RUT del emisor asociado al cobro.
        :return: Respuesta JSON con la información detallada del cobro.
        """
        url = "/pagos/cobros/info/%(codigo)s/%(emisor)s" % {
            'codigo' : codigo,
            'emisor' : emisor
        }
        return self.client.get(url)
