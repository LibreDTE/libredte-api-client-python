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
 - Descargar el PDF de un DTE emitido
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-08-05
"""

# datos a utilizar
url = 'https://libredte.cl'
hash = ''
rut = 76192083
dte = 33
folio = 394
papelContinuo = 0 # =75 ó =80 para papel contínuo
copias_tributarias = 1
copias_cedibles = 1
cedible = int(bool(copias_cedibles)) # =1 genera cedible, =0 no genera cedible

# módulos que se usarán
from os import sys
from libredte.sdk import LibreDTE

# crear cliente
Cliente = LibreDTE(hash, url)

# obtener el PDF del DTE
opciones = '?papelContinuo='+str(papelContinuo)+'&copias_tributarias='+str(copias_tributarias)+'&copias_cedibles='+str(copias_cedibles)+'&cedible='+str(cedible)
pdf = Cliente.get('/dte/dte_emitidos/pdf/'+str(dte)+'/'+str(folio)+'/'+str(rut)+opciones)
if pdf.status_code!=200 :
    sys.exit('Error al generar PDF del DTE: '+pdf.json())

# guardar PDF en el disco
with open('005-dte_emitido_pdf.pdf', 'wb') as f:
    f.write(pdf.content)
