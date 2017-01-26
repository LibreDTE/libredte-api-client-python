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

import requests, json

"""
Clase con las funcionalidades para integrar con LibreDTE
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-06-22
"""
class LibreDTE:

    def __init__ (self, hash, url = 'https://libredte.cl', ssl_check = True) :
        """Constructor de la clase LibreDTE
        :param hash: hash Hash de autenticación del usuario
        :param url: Host con la dirección web base de LibreDTE
        :param ssl_check: si se debe o no verificar el certificado SSL del host
        """
        self.url = url
        self.auth = requests.auth.HTTPBasicAuth(hash, 'X')
        self.ssl_check = ssl_check

    def get (self, api) :
        """Método que consume un servicio web de LibreDTE a través de GET
        :param api: Recurso de la API que se desea consumir (sin /api)
        """
        return requests.get(self.url+'/api'+api, auth=self.auth, verify=self.ssl_check)

    def post (self, api, data = None) :
        """Método que consume un servicio web de LibreDTE a través de POST
        :param api: Recurso de la API que se desea consumir (sin /api)
        :param data: Datos que se codificarán como JSON y se enviarán al recurso
        """
        if isinstance(data, str) :
            data_json = data
        else :
            data_json = json.dumps(data)
        return requests.post(self.url+'/api'+api, data_json, auth=self.auth, verify=self.ssl_check)
