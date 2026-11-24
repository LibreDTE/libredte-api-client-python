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

"""Pruebas del pago de cobros de DTE temporales."""

from datetime import datetime

from tests.pagos_cobros_masivos.abstract_pagos_cobros_masivos import (
    AbstractPagosCobrosMasivos,
)
from tests.respuestas import leer_cobro, leer_objeto


class TestPagarCobroDteTemp(AbstractPagosCobrosMasivos):

    """Clase de pruebas para pagar cobros de DTEs temporales."""

    def test_pagar_cobro_dte_temp(self) -> None:
        """
        El cobro pagado queda con la fecha del pago.

        IMPORTANTE: El cobro queda pagado en la cuenta del contribuyente.
        """
        cobro = leer_cobro(self._buscar_cobro_dte_temp(self.contribuyente_rut))
        pago = {
            'medio': 'efectivo',
            'fecha': datetime.now().astimezone().strftime('%Y-%m-%d'),
        }
        pagado = leer_objeto(
            self.cobros.pagar_cobro(
                cobro['codigo'],
                self.contribuyente_rut,
                pago,
            ),
        )
        self.assertEqual(pagado['codigo'], cobro['codigo'])
        self.assertEqual(pagado['pagado'], pago['fecha'])
        self._mostrar('cobro', pagado)
