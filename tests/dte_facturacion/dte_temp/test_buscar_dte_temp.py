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

"""Pruebas de la búsqueda de un DTE temporal específico."""

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_dte_temporal


class TestBuscarDteTemp(AbstractDteFacturacion):

    """Clase de pruebas para buscar un DTE temporal específico."""

    def test_buscar_dte_temp(self) -> None:
        """La búsqueda entrega el DTE temporal recién emitido."""
        dte_temporal = self._emitir_dte_temporal(self.datos)
        encontrado = leer_dte_temporal(
            self.dte.get_dte_temporal(
                dte_temporal['receptor'],
                dte_temporal['dte'],
                dte_temporal['codigo'],
                self.contribuyente_rut,
            ),
        )
        self.assertEqual(encontrado['codigo'], dte_temporal['codigo'])
        self.assertEqual(str(encontrado['dte']), str(dte_temporal['dte']))
        self._mostrar('dte', encontrado)
