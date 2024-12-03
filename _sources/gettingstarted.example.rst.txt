Ejemplo
============

Ejemplo de Generar un DTE temporal
----------------------------------

Antes de probar, integrar y/o utilizar el cliente de API, necesitas haber definido previamente las variables de entorno.

.. seealso::
    Para más información sobre este paso, referirse al la guía en `Configuración <gettingstarted.setup>`_.

El siguiente es un ejemplo básico de cómo emitir un DTE usando el cliente de API de LibreDTE:

.. code:: python

    # Importación de biblioteca de DTE del API Client, y biblioteca json.
    from libredte.api_client.dte import Dte
    from datetime import datetime
    import json

    # Instanciación de cliente de API
    dte = Dte()

    # RUT del emisor, con DV.
    emisor_rut = '12345678-9'

    # Datos del DTE temporal a crear.
    datos = {
        'Encabezado': {
            'IdDoc': {
                'TipoDTE': 33,
                'FchEmis': datetime.now().strftime("%Y-%m-%d"),
            },
            'Emisor': {
                'RUTEmisor': emisor_rut
            },
            'Receptor': {
                'RUTRecep': '60803000-K',
                'RznSocRecep': 'Servicio de Impuestos Internos (SII)',
                'GiroRecep': 'Administración Pública',
                'Contacto': '+56 2 3252 5575',
                'CorreoRecep': 'facturacionmipyme@sii.cl',
                'DirRecep': 'Teatinos 120',
                'CmnaRecep': 'Santiago',
            }
        },
        'Detalle': [
            {
                #'IndExe': 1, # para items exentos
                'NmbItem': 'Asesoría de LibreDTE',
                'QtyItem': 1,
                'PrcItem': 1000,
            }
        ],
        'Referencia': [
            {
                'TpoDocRef': 801,
                'FolioRef': 'OC123',
                'FchRef': '2015-10-01',
            }
        ],
    }

    # Se efectua la solicitud HTTP llamando a un método del API client,
    # y se guarda la respuesta.
    response = dte.emitir_dte_temporal(datos)
    # Se transforma el contenido a formato JSON.
    dte_temporal = response.json()
    print('\nGENERAR DTE TEMP', json.dumps(dte_temporal),'\n')

    # Se genera un DTE real utilizando datos del DTE temporal recientemente
    # generado.
    dte_real = dte.emitir_dte_real(dte_temporal)
    print('\nGENERAR DTE REAL', json.dumps(dte_real),'\n')

.. seealso::
    Para saber más sobre los parámetros posibles y el cómo consumir los servicios de la API, referirse a la `documentación de LibreDTE. <https://developers.libredte.cl/>`_
