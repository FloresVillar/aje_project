#### Big MAgic - Efletex T1.pptx 
Módulo de Transportes: Integración Big Magic - Efletex

Este documento detalla la integración técnica entre el ERP **Big Magic** (Módulo de Cadena) y la **Plataforma de EFletex** para la automatización de fletes.

##### 1. Publicar Anuncio
El flujo permite la creación y envío automático de requerimientos de servicio.

* **Usuario**: Crea el Requerimiento de Servicio de Flete en Big Magic.
* **Proceso Automático**: Envía el anuncio a la plataforma de EFletex.
* **Respuesta**: EFletex retorna el **ID Anuncio** de forma automática.

##### 2. Actualizar Estado del Anuncio
Sincronización de estados entre plataformas mediante tareas programadas (Jobs).

* **Estados de Negociación**:
    * Transportista publica oferta -> Usuario acepta oferta.
    * **Job (cada 5 minutos)**: Retorna el estado y actualiza en Big Magic a **Negociado**.
* **Estados de Anulación**:
    * Usuario anula el anuncio en Big Magic.
    * **Job (cada 5 minutos)**: Retorna el estado y actualiza en Big Magic a **Anulado**.

##### 3. Servicios Técnicos (Endpoints y SP)

| ID | Descripción | SP en Big Magic (BM) | Servicio Efletex (Test/API) |
| :--- | :--- | :--- | :--- |
| 1 | Publicar Anuncio | `PR_ERP_COM_QRY_WS_PUBLICARENVIO` | `https://efletexfiles.com/apiV2/publicar-envio` |
| 2 | Comprobar Estatus de envío | `PR_ERP_COM_QRY_WS_ESTADOANUNCIO_V2` | `https://efletexfiles.com/apiV2/status-envio` |
| 3 | Documentación envío | `PR_ERP_COM_QRY_WS_DOCUMENTOSENVIO` | `https://efletexfiles.com/documentacion-envio` |

##### 4. Componentes de Sincronización (Backend)

* **SQL Job**: `MX33_WS_ESTADOANUNCIO_EFLETEX` (Encargado de la ejecución recurrente cada 5 minutos).
La auditoría de mensajes se realiza mediante la tabla correomsg, filtrando por sucursal (33), compañía (1) y el identificador de proceso WS_EFLETEX, ordenando por fecha descendente para obtener el rastro más reciente de las tramas XML/JSON de entrada y salida.

