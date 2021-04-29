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

import requests, json, base64, os


"""
Clase con las funcionalidades para integrar con LibreDTE
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2021-03-27
"""
class LibreDTE:

    def __init__(self, hash = None, url = None, ssl_check = True):
        """Constructor de la clase LibreDTE
        :param hash: hash Hash de autenticación del usuario
        :param url: Host con la dirección web base de LibreDTE
        :param ssl_check: si se debe o no verificar el certificado SSL del host
        """
        if hash is None:
            hash = str(os.getenv('LIBREDTE_HASH'))
        if url is None:
            url = str(os.getenv('LIBREDTE_URL', 'https://libredte.cl'))
        self.url = url
        self.auth = requests.auth.HTTPBasicAuth(hash, 'X')
        self.ssl_check = ssl_check
        self.rut = os.getenv('LIBREDTE_RUT')
        if self.rut is not None:
            self.rut = int(self.rut)

    def get(self, api):
        """Método que consume un servicio web de LibreDTE a través de GET
        :param api: Recurso de la API que se desea consumir (sin /api)
        """
        return requests.get(self.url + '/api' + api, auth=self.auth, verify=self.ssl_check)

    def post(self, api, data = None):
        """Método que consume un servicio web de LibreDTE a través de POST
        :param api: Recurso de la API que se desea consumir (sin /api)
        :param data: Datos que se codificarán como JSON y se enviarán al recurso
        """
        if isinstance(data, str):
            data_json = data
        else:
            data_json = json.dumps(data)
        return requests.post(self.url + '/api' + api, data_json, auth=self.auth, verify=self.ssl_check)

    def create_link(self, resource, rut = None):
        """Método para crear un enlace que apunte a la plataforma de LibreDTE
        :param rut: RUT del contribuyente en LibreDTE con el que se quiere usar el recurso
        :param resource: recurso al que se desea acceder en la plataforma de LibreDTE
        """
        if rut is None:
            rut = self.rut
        resource_base64 = base64.b64encode(resource.encode('utf-8')).decode('utf-8')
        return self.url + '/dte/contribuyentes/seleccionar/' + str(rut) + '/' + str(resource_base64)
