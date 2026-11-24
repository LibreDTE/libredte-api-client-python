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

"""Pruebas del envío por correo de un DTE real."""

import unittest
from os import getenv
from typing import ClassVar

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)


class TestEnviarEmailDteReal(AbstractDteFacturacion):

    """Clase de pruebas para enviar por correo un DTE emitido (real)."""

    # Correo al que se envía el DTE (variable de entorno TEST_EMAIL).
    email: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        """Prepara el cliente y el correo de destino de la prueba."""
        email = getenv('TEST_EMAIL', '').strip()
        if not email:
            msg = 'Se debe configurar la variable de entorno TEST_EMAIL.'
            raise unittest.SkipTest(msg)
        cls.email = email
        super().setUpClass()

    def test_enviar_email_dte_real(self) -> None:
        """
        El DTE emitido se envía por correo a TEST_EMAIL.

        IMPORTANTE: Si el receptor del DTE no tiene correo, la API guarda
        TEST_EMAIL como correo del receptor.
        """
        documento = self._primer_dte_emitido()
        dte = documento['dte']
        folio = documento['folio']
        rut = self.contribuyente_rut
        datos_email = {
            'emails': [self.email],
            'asunto': (
                '[LibreDTE API Client Test] Envío de DTE '
                f'T{dte}F{folio} de {rut}'
            ),
            'mensaje': (
                'LibreDTE API Client Test: DTE ID '
                f'T{dte}F{folio} de {rut}.'
            ),
            'pdf': True,
            'cedible': True,
            'papelContinuo': False,
        }
        response = self.dte.dte_real_enviar_email(dte, folio, rut, datos_email)
        self.assertEqual(response.status_code, 200)
        self._mostrar('email', response.text)
