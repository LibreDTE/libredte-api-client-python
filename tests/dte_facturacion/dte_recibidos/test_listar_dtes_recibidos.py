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

"""Pruebas del listado de DTE recibidos."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_dtes_recibidos


class TestListarDtesRecibidos(AbstractDteFacturacion):

    """Clase de pruebas para listar DTEs recibidos."""

    def test_listar_dtes_recibidos(self) -> None:
        """El listado solo incluye DTE del rango de fechas buscado."""
        documentos = leer_dtes_recibidos(
            self._listar_dtes_recibidos(self.contribuyente_rut),
        )
        for documento in documentos:
            self.assertGreaterEqual(
                documento['fecha'],
                self.filtros['fecha_desde'],
            )
            self.assertLessEqual(
                documento['fecha'],
                self.filtros['fecha_hasta'],
            )
        self._mostrar('dtes_recibidos', documentos)
