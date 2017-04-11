#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LibreDTE
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o
modificarlo bajo los términos de la Licencia Pública General Affero de GNU
publicada por la Fundación para el Software Libre, ya sea la versión
3 de la Licencia, o (a su elección) cualquier versión posterior de la
misma.

Este programa se distribuye con la esperanza de que sea útil, pero
SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita
MERCANTIL o de APTITUD PARA UN PROPÓSITO DETERMINADO.
Consulte los detalles de la Licencia Pública General Affero de GNU para
obtener una información más detallada.

Debería haber recibido una copia de la Licencia Pública General Affero de GNU
junto a este programa.
En caso contrario, consulte <http://www.gnu.org/licenses/agpl.html>.
"""

"""
Ejemplo que muestra los pasos para:
 - Obtener el timbre en formato PNG de un DTE emitido
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-04-11
"""

# datos a utilizar
url = 'https://libredte.cl'
hash = ''
rut = 76192083
dte = 33
folio = 42

# módulos que se usarán
from os import sys
from libredte.sdk import LibreDTE

# crear cliente
Cliente = LibreDTE(hash, url)

# descargar timbre de dte emitido
timbre_png = Cliente.get('/dte/dte_emitidos/ted/'+str(dte)+'/'+str(folio)+'/'+str(rut))
if timbre_png.status_code!=200 :
    sys.exit('Error al obtener el timbre del DTE emitido: '+timbre_png.json())

# guardar PMG en el disco
with open('001-dte_emitido_timbre.png', 'wb') as f:
    f.write(timbre_png.content)
