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

"""Pruebas de la búsqueda de un DTE real específico."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_dte_emitido


class TestBuscarDteReal(AbstractDteFacturacion):

    """Clase de pruebas para buscar un DTE real específico."""

    def test_buscar_dte_real(self) -> None:
        """La búsqueda entrega el DTE real solicitado."""
        documento = self._primer_dte_emitido()
        encontrado = leer_dte_emitido(
            self.dte.get_dte_real(
                documento['dte'],
                documento['folio'],
                self.contribuyente_rut,
            ),
        )
        self.assertEqual(str(encontrado['folio']), str(documento['folio']))
        self.assertEqual(str(encontrado['dte']), str(documento['dte']))
        self._mostrar('dte', encontrado)
