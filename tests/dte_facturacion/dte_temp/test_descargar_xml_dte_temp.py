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

"""Pruebas de la descarga del XML de un DTE temporal."""

import os
from base64 import b64decode
from xml.etree import ElementTree

from tests.dte_facturacion.abstract_dte_facturacion import (
    AbstractDteFacturacion,
)
from tests.respuestas import leer_texto


class TestDescargarXmlDteTemp(AbstractDteFacturacion):

    """Clase de pruebas para descargar un XML de un DTE temporal."""

    def _guardar(self, carpeta: str, nombre: str, contenido: bytes) -> str:
        """
        Guarda un archivo descargado en tests/archivos/dte_facturacion.

        :param str carpeta: Subcarpeta del archivo.
        :param str nombre: Nombre del archivo.
        :param bytes contenido: Contenido del archivo.
        :return: Ruta del archivo guardado.
        """
        tests_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
        output_dir = os.path.join(
            tests_dir,
            'archivos',
            'dte_facturacion',
            carpeta,
        )
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, nombre)
        with open(filename, 'wb') as f:
            f.write(contenido)
        return filename

    def _leer_xml(self, contenido: bytes) -> ElementTree.Element:
        """
        Lee un XML del SII (codificado en ISO-8859-1).

        :param bytes contenido: XML.
        :return: Elemento raíz del XML.
        """
        parser = ElementTree.XMLParser(encoding='ISO-8859-1')
        return ElementTree.fromstring(contenido, parser=parser)

    def test_descargar_xml_dte_temp(self) -> None:
        """El XML del DTE temporal (en base64) es un XML de un DTE."""
        dte_temporal = self._emitir_dte_temporal(self.datos)
        response = self.dte.get_xml_dte_temporal(
            dte_temporal['receptor'],
            dte_temporal['dte'],
            dte_temporal['codigo'],
            dte_temporal['emisor'],
        )
        xml = b64decode(leer_texto(response), validate=True)
        self.assertIn('DTE', self._leer_xml(xml).tag)
        # LIBREDTE_[rut_emisor]_[dte]_[codigo].xml
        filename = self._guardar(
            'dte_temp_xml',
            f'LIBREDTE_{self.contribuyente_rut}_{dte_temporal['dte']}_'
            f'{dte_temporal['codigo']}.xml',
            xml,
        )
        self._mostrar('filename', filename)
