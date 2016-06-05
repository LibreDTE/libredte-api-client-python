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

import requests, json

"""
Clase con las funcionalidades para integrar con LibreDTE
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-06-05
"""
class LibreDTE () :

    """
    Constructor de la clase LibreDTE
    @param hash Hash de autenticación del usuario
    @param host Host con la dirección web base de LibreDTE
    @author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
    @version 2016-06-05
    """
    def __init__ (self, hash, url = 'https://libredte.cl', ssl_check = True) :
        self.url = url
        self.auth = requests.auth.HTTPBasicAuth(hash, 'X')
        self.ssl_check = ssl_check

    """
    Método que consume un servicio web de LibreDTE a través de POST
    @author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
    @version 2016-06-05
    """
    def post (self, api, data = None) :
        return requests.post(self.url+'/api'+api, json.dumps(data), auth=self.auth, verify=self.ssl_check)
