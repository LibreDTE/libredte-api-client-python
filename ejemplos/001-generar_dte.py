#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LibreDTE
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

"""
Ejemplo que muestra los pasos para:
 - Emitir DTE temporal
 - Generar DTE real a partir del temporal
 - Obtener PDF a partir del DTE real
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-11-20
"""

# datos a utilizar
url = 'https://libredte.cl'
hash = ''
dte = {
    'Encabezado': {
        'IdDoc': {
            'TipoDTE': 33,
        },
        'Emisor': {
            'RUTEmisor': '76192083-9',
        },
        'Receptor': {
            'RUTRecep': '66666666-6',
            'RznSocRecep': 'Persona sin RUT',
            'GiroRecep': 'Particular',
            'DirRecep': 'Santiago',
            'CmnaRecep': 'Santiago',
        },
    },
    'Detalle': [
        {
            'NmbItem': 'Producto 1',
            'QtyItem': 2,
            'PrcItem': 1000,
        },
    ],
}

# módulos que se usarán
from os import sys
from libredte.sdk import LibreDTE

# crear cliente
Cliente = LibreDTE(hash, url)

# crear DTE temporal
emitir = Cliente.post('/dte/documentos/emitir', dte)
if emitir.status_code!=200 :
    sys.exit('Error al emitir DTE temporal: '+emitir.json())

# crear DTE real
generar = Cliente.post('/dte/documentos/generar', emitir.json())
if generar.status_code!=200 :
    sys.exit('Error al generar DTE real: '+generar.json())

# obtener el PDF del DTE
generar_pdf = Cliente.get('/dte/dte_emitidos/pdf/'+str(generar.json()['dte'])+'/'+str(generar.json()['folio'])+'/'+str(generar.json()['emisor']))
if generar_pdf.status_code!=200 :
    sys.exit('Error al generar PDF del DTE: '+generar_pdf.json())

# guardar PDF en el disco
with open('001-generar_dte.pdf', 'wb') as f:
    f.write(generar_pdf.content)
