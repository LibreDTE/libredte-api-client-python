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

"""Pruebas de la eliminación de un DTE temporal."""

from http import HTTPStatus

from libredte.api_client import ApiException
from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_booleano


class TestEliminarDteTemp(AbstractDteFacturacion):

    """Clase de pruebas para probar la función eliminar dte temporal."""

    def test_eliminar_dte_temp(self) -> None:
        """Después de eliminarlo, el DTE temporal ya no existe."""
        dte_temporal = self._emitir_dte_temporal(self.datos)
        identificacion = (
            dte_temporal['receptor'],
            dte_temporal['dte'],
            dte_temporal['codigo'],
            self.contribuyente_rut,
        )
        eliminado = leer_booleano(
            self.dte.delete_dte_temporal(*identificacion),
        )
        self.assertTrue(eliminado)
        with self.assertRaises(ApiException) as contexto:
            self.dte.get_dte_temporal(*identificacion)
        self.assertEqual(contexto.exception.code, HTTPStatus.NOT_FOUND)
        self._mostrar('dte_eliminado', eliminado)
