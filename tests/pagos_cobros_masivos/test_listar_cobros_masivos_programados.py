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

"""Pruebas del listado de cobros."""

from tests.pagos_cobros_masivos.abstract_pagos_cobros_masivos import (
    AbstractPagosCobrosMasivos,
)
from tests.respuestas import leer_lista_objetos


class TestListarCobrosMasivosProgramados(AbstractPagosCobrosMasivos):

    """Clase de pruebas para listar cobros."""

    def test_listar_cobros(self) -> None:
        """El listado de cobros sin pagar no incluye cobros pagados."""
        response = self._listar_cobros(self.contribuyente_rut)
        cobros = leer_lista_objetos(response)
        for cobro in cobros:
            self.assertFalse(cobro.get('pagado'), cobro)
        self._mostrar('cobros', cobros)
