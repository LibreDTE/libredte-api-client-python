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

"""Pruebas de la información del cobro de un DTE temporal."""

from tests.pagos_cobros_masivos.abstract_pagos_cobros_masivos import (
    AbstractPagosCobrosMasivos,
)
from tests.respuestas import leer_cobro


class TestBuscarCobroProgramado(AbstractPagosCobrosMasivos):

    """Clase de pruebas para obtener la información de un cobro."""

    def test_buscar_cobro(self) -> None:
        """La información del cobro de un DTE temporal es la de ese cobro."""
        rut = self.contribuyente_rut
        cobro = leer_cobro(self._buscar_cobro_dte_temp(rut))
        informacion = leer_cobro(
            self.cobros.get_cobro_info(cobro['codigo'], rut),
        )
        self.assertEqual(informacion['codigo'], cobro['codigo'])
        self._mostrar('cobro', informacion)
