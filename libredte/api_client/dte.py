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
from . import ApiBase
from urllib.parse import urlencode

class Dte(ApiBase):
    """
    Clase para interactuar con los endpoints de DTE de la API.

    Esta clase hereda de ApiBase y proporciona métodos específicos para operaciones relacionadas con DTE,
    como obtener información del receptor, emitir y generar DTEs, tanto temporales como reales, y enviar DTEs por correo electrónico.
    """

    def emitir_dte_temporal(self, dte_temporal, filtros=None):
        """
        Emite un DTE temporal.

        :param dict dte_temporal: Datos del DTE temporal a emitir.
        :param dict filtros: Parámetros adicionales para la consulta (opcional).
        :return: Respuesta JSON del DTE temporal emitido.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.post(f'/dte/documentos/emitir?{filtros}', data=dte_temporal)

    def get_dte_temporal(self, receptor, dte, codigo, emisor, filtros=None):
        """
        Obtiene información de un DTE temporal específico.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE temporal.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta (opcional).
        :return: Respuesta JSON con la información del DTE temporal.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.get(f'/dte/dte_tmps/info/{receptor}/{dte}/{codigo}/{emisor}?{filtros}')

    def emitir_dte_real(self, dte_real, filtros=None):
        """
        Genera un DTE real a partir de los datos proporcionados, correspondientes aun dte temporal.

        :param dict dte_real: Datos del DTE real a generar.
        :return: Respuesta JSON del DTE real generado.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.post(f'/dte/documentos/generar?{filtros}', data=dte_real)

    def get_dte_real(self, dte, folio, emisor, filtros=None):
        """
        Obtiene información de un DTE real específico.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta (opcional).
        :return: Respuesta JSON con la información del DTE real.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.get(f'/dte/dte_emitidos/info/{dte}/{folio}/{emisor}?{filtros}')

    def dte_temporal_enviar_email(self, receptor, dte, codigo, emisor, data_email):
        """
        Envía por correo electrónico un DTE temporal.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE temporal.
        :param str emisor: RUT del emisor.
        :param dict data_email: Datos del correo electrónico a enviar.
        :return: Respuesta JSON del resultado del envío.
        """
        return self.client.post(f'/dte/dte_tmps/enviar_email/{receptor}/{dte}/{codigo}/{emisor}', data=data_email)

    def dte_real_enviar_email(self, dte, folio, emisor, data_email):
        """
        Envía por correo electrónico un DTE real.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict data_email: Datos del correo electrónico a enviar.
        :return: Respuesta JSON del resultado del envío.
        """
        return self.client.post(f'/dte/dte_emitidos/enviar_email/{dte}/{folio}/{emisor}', data=data_email)

    def get_pdf_real(self, dte, folio, emisor, filtros=None):
        """
        Obtiene el PDF de un DTE real específico.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta (opcional).
        :return: Respuesta con el PDF del DTE real.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.get(f'/dte/dte_emitidos/pdf/{dte}/{folio}/{emisor}?{filtros}')

    def get_dte_emitidos(self, emisor, filtros):
        """
        Busca DTEs emitidos por un emisor específico utilizando filtros de búsqueda.

        :param str emisor: RUT del emisor.
        :param dict filtros: Filtros de búsqueda para aplicar.
        :return: Respuesta JSON con los DTEs emitidos que coinciden con los filtros.
        """
        return self.client.post(f'/dte/dte_emitidos/buscar/{emisor}', data=filtros)

    def dte_emitidos_actualizar_estado(self, dte, folio, emisor, filtros=None):
        """
        Actualiza el estado de un DTE emitido.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la actualización de estado (opcional).
        :return: Respuesta JSON con el resultado de la actualización del estado del DTE.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.get(f'/dte/dte_emitidos/actualizar_estado/{dte}/{folio}/{emisor}?{filtros}')

    def dte_emitidos_consultar(self, filtros):
        """
        Consulta los DTEs emitidos utilizando filtros de búsqueda.

        :param dict filtros: Filtros de búsqueda para aplicar en la consulta.
        :return: Respuesta JSON con los DTEs emitidos que coinciden con los filtros.
        """
        return self.client.post('/dte/dte_emitidos/consultar', data=filtros)

    def dte_emitidos_ted(self, dte, folio, emisor, filtros=None):
        """
        Obtiene el TED (Timbre Electrónico de DTE) de un DTE emitido.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta (opcional).
        :return: Respuesta con el TED del DTE solicitado.
        """
        filtros = '' if filtros is None else urlencode(filtros)
        return self.client.get(f'/dte/dte_emitidos/ted/{dte}/{folio}/{emisor}?{filtros}')