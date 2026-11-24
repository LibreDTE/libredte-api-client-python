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

"""Pruebas de la emisión de un DTE temporal."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)


class TestEmitirDteTemp(AbstractDteFacturacion):

    """Clase de pruebas que permite emitir un DTE temporal."""

    def test_emitir_dte_temp(self) -> None:
        """Al emitir, la API entrega el tipo y el código del DTE temporal."""
        dte_temporal = self._emitir_dte_temporal(self.datos)
        self.assertEqual(int(dte_temporal['dte']), 33)
        self.assertTrue(dte_temporal['codigo'])
        self._mostrar('dte_temporal', dte_temporal)
