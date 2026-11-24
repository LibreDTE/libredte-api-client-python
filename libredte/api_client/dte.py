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

"""Wrapper de los recursos de DTE de la API de LibreDTE."""

from collections.abc import Mapping

import requests

from . import ApiBase


class Dte(ApiBase):

    """
    Clase para interactuar con los endpoints de DTE de la API.

    Esta clase hereda de ApiBase y proporciona métodos específicos para
    operaciones relacionadas con DTE: emitir y generar DTEs, tanto temporales
    como reales, buscarlos, descargar su PDF y XML, y enviarlos por correo
    electrónico.
    """

    def emitir_dte_temporal(
        self,
        dte_temporal: Mapping[str, object],
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Realiza la emisión de un DTE temporal.

        :param dict dte_temporal: Datos del DTE temporal a emitir.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta JSON del DTE temporal emitido.
        """
        query = self._query(filtros)
        url = f'/dte/documentos/emitir?{query}'
        return self.client.post(url, data=dte_temporal)

    def get_dte_temporal(
        self,
        receptor: str | int,
        dte: str | int,
        codigo: str,
        emisor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Obtiene información de un DTE temporal específico.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE temporal.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta JSON con la información del DTE temporal.
        """
        query = self._query(filtros)
        ruta = self._ruta('/dte/dte_tmps/info', receptor, dte, codigo, emisor)
        url = f'{ruta}?{query}'
        return self.client.get(url)

    def delete_dte_temporal(
        self,
        receptor: str | int,
        dte: str | int,
        codigo: str,
        emisor: str | int,
    ) -> requests.Response:
        """
        Elimina un DTE temporal específico.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE temporal.
        :param str emisor: RUT del emisor.
        :return: Respuesta JSON con un boolean que retorna verdadero si se
            eliminó el DTE temporal.
        """
        url = self._ruta(
            '/dte/dte_tmps/eliminar',
            receptor,
            dte,
            codigo,
            emisor,
        )
        return self.client.get(url)

    def emitir_dte_real(
        self,
        dte_real: Mapping[str, object],
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Genera un DTE real a partir de los datos de un DTE temporal.

        :param dict dte_real: Datos del DTE real a generar.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta JSON del DTE real generado.
        """
        query = self._query(filtros)
        url = f'/dte/documentos/generar?{query}'
        return self.client.post(url, data=dte_real)

    def get_dte_real(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Obtiene información de un DTE real específico.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta JSON con la información del DTE real.
        """
        query = self._query(filtros)
        ruta = self._ruta('/dte/dte_emitidos/info', dte, folio, emisor)
        url = f'{ruta}?{query}'
        return self.client.get(url)

    def dte_temporal_enviar_email(
        self,
        receptor: str | int,
        dte: str | int,
        codigo: str,
        emisor: str | int,
        data_email: Mapping[str, object],
    ) -> requests.Response:
        """
        Envía por correo electrónico un DTE temporal.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE temporal.
        :param str emisor: RUT del emisor.
        :param dict data_email: Datos del correo electrónico a enviar.
        :return: Respuesta JSON del resultado del envío.
        """
        url = self._ruta(
            '/dte/dte_tmps/enviar_email',
            receptor,
            dte,
            codigo,
            emisor,
        )
        return self.client.post(url, data=data_email)

    def dte_real_enviar_email(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
        data_email: Mapping[str, object],
    ) -> requests.Response:
        """
        Envía por correo electrónico un DTE real.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict data_email: Datos del correo electrónico a enviar.
        :return: Respuesta JSON del resultado del envío.
        """
        url = self._ruta('/dte/dte_emitidos/enviar_email', dte, folio, emisor)
        return self.client.post(url, data=data_email)

    def get_pdf_dte_real(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Obtiene el PDF de un DTE real específico.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta con el PDF del DTE real.
        """
        query = self._query(filtros)
        ruta = self._ruta('/dte/dte_emitidos/pdf', dte, folio, emisor)
        url = f'{ruta}?{query}'
        return self.client.get(url)

    def get_dte_emitidos(
        self,
        emisor: str | int,
        filtros: Mapping[str, object],
    ) -> requests.Response:
        """
        Busca DTEs emitidos por un emisor usando filtros de búsqueda.

        :param str emisor: RUT del emisor.
        :param dict filtros: Filtros de búsqueda para aplicar.
        :return: Respuesta JSON con los DTEs emitidos que coinciden con los
            filtros.
        """
        url = self._ruta('/dte/dte_emitidos/buscar', emisor)
        return self.client.post(url, data=filtros)

    def dte_emitidos_actualizar_estado(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Actualiza el estado de un DTE emitido.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la actualización de
            estado (opcional).
        :return: Respuesta JSON con el resultado de la actualización del
            estado del DTE.
        """
        query = self._query(filtros)
        ruta = self._ruta(
            '/dte/dte_emitidos/actualizar_estado',
            dte,
            folio,
            emisor,
        )
        url = f'{ruta}?{query}'
        return self.client.get(url)

    def dte_emitidos_consultar(
        self,
        filtros: Mapping[str, object],
    ) -> requests.Response:
        """
        Consulta los DTEs emitidos utilizando filtros de búsqueda.

        :param dict filtros: Filtros de búsqueda para aplicar en la consulta.
        :return: Respuesta JSON con los DTEs emitidos que coinciden con los
            filtros.
        """
        return self.client.post('/dte/dte_emitidos/consultar', data=filtros)

    def dte_emitidos_ted(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Obtiene el TED (Timbre Electrónico de DTE) de un DTE emitido.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta con el TED del DTE solicitado.
        """
        query = self._query(filtros)
        ruta = self._ruta('/dte/dte_emitidos/ted', dte, folio, emisor)
        url = f'{ruta}?{query}'
        return self.client.get(url)

    def get_dte_temporales(
        self,
        emisor: str | int,
        filtros: Mapping[str, object],
    ) -> requests.Response:
        """
        Obtiene un listado de DTEs temporales.

        :param str emisor: RUT del emisor.
        :param dict filtros: Filtros de búsqueda para aplicar.
        :return: Respuesta JSON con la lista del DTEs temporales.
        """
        url = self._ruta('/dte/dte_tmps/buscar', emisor)
        return self.client.post(url, data=filtros)

    def get_dte_recibidos(
        self,
        receptor: str | int,
        filtros: Mapping[str, object],
    ) -> requests.Response:
        """
        Obtiene un listado de DTEs recibidos.

        :param str receptor: RUT del receptor.
        :param dict filtros: Filtros de búsqueda para aplicar.
        :return: Respuesta JSON con la lista del DTEs recibidos.
        """
        url = self._ruta('/dte/dte_recibidos/buscar', receptor)
        return self.client.post(url, data=filtros)

    def get_pdf_dte_temporal(
        self,
        receptor: str | int,
        dte: str | int,
        codigo: str,
        emisor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Obtiene el PDF de un DTE temporal específico.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE.
        :param str emisor: RUT del emisor.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta con el PDF del DTE temporal.
        """
        query = self._query(filtros)
        ruta = self._ruta('/dte/dte_tmps/pdf', receptor, dte, codigo, emisor)
        url = f'{ruta}?{query}'
        return self.client.get(url)

    def get_xml_dte_temporal(
        self,
        receptor: str | int,
        dte: str | int,
        codigo: str,
        emisor: str | int,
    ) -> requests.Response:
        """
        Obtiene un XML de un DTE temporal.

        :param str receptor: RUT del receptor.
        :param str dte: Tipo de DTE.
        :param str codigo: Código del DTE temporal.
        :param str emisor: RUT del emisor.
        :return: Respuesta codificada en base64 con el XML del DTE temporal.
        """
        url = self._ruta('/dte/dte_tmps/xml', receptor, dte, codigo, emisor)
        return self.client.get(url)

    def get_xml_dte_real(
        self,
        dte: str | int,
        folio: str | int,
        emisor: str | int,
    ) -> requests.Response:
        """
        Obtiene un XML de un DTE emitido.

        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE emitido.
        :param str emisor: RUT del emisor.
        :return: Respuesta codificada en base64 con el XML del DTE emitido.
        """
        url = self._ruta('/dte/dte_emitidos/xml', dte, folio, emisor)
        return self.client.get(url)

    def get_xml_dte_recibido(
        self,
        emisor: str | int,
        dte: str | int,
        folio: str | int,
        receptor: str | int,
    ) -> requests.Response:
        """
        Obtiene un XML de un DTE recibido.

        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE recibido.
        :param str receptor: RUT del receptor.
        :return: Respuesta codificada en base64 con el XML del DTE recibido.
        """
        url = self._ruta(
            '/dte/dte_recibidos/xml',
            emisor,
            dte,
            folio,
            receptor,
        )
        return self.client.get(url)

    def get_dte_recibido(
        self,
        emisor: str | int,
        dte: str | int,
        folio: str | int,
        receptor: str | int,
        filtros: Mapping[str, object] | None = None,
    ) -> requests.Response:
        """
        Obtiene información de un DTE recibido específico.

        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE.
        :param str folio: Folio del DTE recibido.
        :param str receptor: RUT del receptor.
        :param dict filtros: Parámetros adicionales para la consulta
            (opcional).
        :return: Respuesta JSON con la información del DTE recibido.
        """
        query = self._query(filtros)
        ruta = self._ruta(
            '/dte/dte_recibidos/info',
            emisor,
            dte,
            folio,
            receptor,
        )
        url = f'{ruta}?{query}'
        return self.client.get(url)
