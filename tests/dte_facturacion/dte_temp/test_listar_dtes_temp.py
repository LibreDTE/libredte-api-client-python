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

"""Pruebas del listado de DTE temporales."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_dtes_temporales


class TestListarDtesTemp(AbstractDteFacturacion):

    """Clase de pruebas para listar DTEs temporales."""

    def test_listar_dtes_temp(self) -> None:
        """El listado incluye el DTE temporal recién emitido."""
        dte_temporal = self._emitir_dte_temporal(self.datos)
        documentos = leer_dtes_temporales(
            self._listar_dtes_temp(self.contribuyente_rut),
        )
        self.assertIn(
            dte_temporal['codigo'],
            [documento['codigo'] for documento in documentos],
        )
        self._mostrar('dtes_temp', documentos)
