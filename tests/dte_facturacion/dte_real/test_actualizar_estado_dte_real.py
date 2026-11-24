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

"""Pruebas de la actualización del estado de un DTE real."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_objeto


class TestActualizarEstadoDteReal(AbstractDteFacturacion):

    """Clase de pruebas para actualizar el estado de un DTE emitido (real)."""

    def test_actualizar_estado_dte_real(self) -> None:
        """
        La actualización entrega el estado de revisión del DTE en el SII.

        IMPORTANTE: El DTE debe haber sido enviado al SII (tener Track ID).
        """
        documento = self._primer_dte_emitido()
        estado = leer_objeto(
            self.dte.dte_emitidos_actualizar_estado(
                documento['dte'],
                documento['folio'],
                self.contribuyente_rut,
                filtros={'usarWebservice': 1},
            ),
        )
        self.assertIn('revision_estado', estado)
        self._mostrar('estado', estado)
