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

"""Pruebas de la consulta del estado de un DTE real."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_dte_emitido


class TestConsultarEstadoDteReal(AbstractDteFacturacion):

    """Clase de pruebas para consultar el estado de un DTE real."""

    def test_consultar_estado_dte_real(self) -> None:
        """La consulta entrega el DTE real con los datos indicados."""
        documento = self._primer_dte_emitido()
        filtros = {
            'emisor': self.contribuyente_rut,
            'dte': documento['dte'],
            'folio': documento['folio'],
            'fecha': documento['fecha'],
            'total': documento['total'],
        }
        consultado = leer_dte_emitido(
            self.dte.dte_emitidos_consultar(filtros=filtros),
        )
        self.assertEqual(str(consultado['folio']), str(documento['folio']))
        self._mostrar('estado', consultado)
