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

"""Pruebas de la obtención del TED de un DTE real."""

from base64 import b64decode
from xml.etree import ElementTree

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_texto


class TestObtenerTedDteReal(AbstractDteFacturacion):

    """Clase de pruebas para obtener el TED de un documento emitido."""

    def _leer_xml(self, contenido: bytes) -> ElementTree.Element:
        """
        Lee un XML del SII (codificado en ISO-8859-1).

        :param bytes contenido: XML.
        :return: Elemento raíz del XML.
        """
        parser = ElementTree.XMLParser(encoding='ISO-8859-1')
        return ElementTree.fromstring(contenido, parser=parser)

    def test_dte_ted(self) -> None:
        """El TED en formato XML (en base64) es un XML con raíz TED."""
        documento = self._primer_dte_emitido()
        response = self.dte.dte_emitidos_ted(
            documento['dte'],
            documento['folio'],
            self.contribuyente_rut,
            # Opciones: png (defecto), bmp, xml
            filtros={'formato': 'xml'},
        )
        ted = b64decode(leer_texto(response), validate=True)
        self.assertTrue(self._leer_xml(ted).tag.endswith('TED'))
        self._mostrar('ted', ted.decode('ISO-8859-1'))
