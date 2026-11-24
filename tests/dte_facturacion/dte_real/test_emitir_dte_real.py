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

"""Pruebas de la emisión de un DTE real."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_dte_emitido, leer_objeto


class TestEmitirDteReal(AbstractDteFacturacion):

    """Clase de pruebas para emitir un DTE real."""

    def test_emitir_dte_real(self) -> None:
        """
        Genera un DTE real (con folio) a partir de un DTE temporal.

        IMPORTANTE: Para emitir un DTE real, se necesita estar habilitado para
        hacerlo, con una firma electrónica.
        """
        dte_temporal = self._emitir_dte_temporal(self.datos)
        detalle = leer_objeto(
            self.dte.get_dte_temporal(
                dte_temporal['receptor'],
                dte_temporal['dte'],
                dte_temporal['codigo'],
                dte_temporal['emisor'],
            ),
        )
        dte_real = leer_dte_emitido(self.dte.emitir_dte_real(detalle))
        self.assertEqual(int(dte_real['dte']), 33)
        self.assertTrue(dte_real['folio'])
        self._mostrar('dte_real', dte_real)
