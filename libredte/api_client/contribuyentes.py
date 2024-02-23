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

class Contribuyentes(ApiBase):
    """
    Clase para interactuar con los endpoints de contribuyentes de la API.

    Ofrece métodos para obtener información de contribuyentes específicos,
    basándose en su RUT.
    """

    def get_contribuyente(self, rut):
        """
        Obtiene la información de un contribuyente específico.

        Realiza una solicitud GET para buscar información sobre un contribuyente
        dado su RUT. Esta información puede incluir datos como el nombre del
        contribuyente, dirección, y otros detalles relevantes.

        :param str rut: RUT del contribuyente a buscar.
        :return: Respuesta JSON con la información del contribuyente.
        """
        return self.client.get(f'/dte/contribuyentes/info/{rut}')
