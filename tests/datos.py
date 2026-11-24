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

"""Datos de los DTE que emiten las pruebas."""

from datetime import datetime
from os import getenv


def datos_dte_temporal(rut_emisor: str) -> dict[str, object]:
    """
    Arma los datos de una factura (DTE 33) de prueba para el SII.

    La fecha de emisión es la de hoy, o la de la variable de entorno
    TEST_DTE_FACTURAR_FECHA_EMISION.

    :param str rut_emisor: RUT del emisor, con dígito verificador.
    :return: Datos del DTE para emitirlo como temporal.
    """
    fecha_emision = getenv(
        'TEST_DTE_FACTURAR_FECHA_EMISION',
        datetime.now().astimezone().strftime('%Y-%m-%d'),
    ).strip()
    return {
        'Encabezado': {
            'IdDoc': {
                'TipoDTE': 33,
                'FchEmis': fecha_emision,
            },
            'Emisor': {
                'RUTEmisor': rut_emisor,
            },
            'Receptor': {
                'RUTRecep': '60803000-K',
                'RznSocRecep': 'Servicio de Impuestos Internos (SII)',
                'GiroRecep': 'Administración Pública',
                'Contacto': '+56 2 3252 5575',
                'CorreoRecep': 'facturacionmipyme@sii.cl',
                'DirRecep': 'Teatinos 120',
                'CmnaRecep': 'Santiago',
            },
        },
        'Detalle': [
            {
                # Para ítems exentos agregar IndExe con valor 1.
                'NmbItem': 'Asesoría de LibreDTE',
                'QtyItem': 1,
                'PrcItem': 1000,
            },
        ],
        'Referencia': [
            {
                'TpoDocRef': 801,
                'FolioRef': 'OC123',
                'FchRef': '2015-10-01',
            },
        ],
    }
