# Integraciones EDI (REST)

## Integración de pedidos EDI

El registro de pedidos se realiza en 2 pasos los cuales se describen a continuación:

1. Ejecución del Recurso - Registra Pedidos (REST)
2. Procesamiento de pedidos

## 1. Recurso - Registra Pedidos (REST)

### 1. Descripción
* Recurso que registra en la MXBDAJE los pedidos que llegaron vía EDI, para su procesamiento posterior en la bd, los pedidos están resguardados en un bucket de S3.
* La ejecución de este endpoint esta programa en AWS.

### 2. Ruta Base
* **DEV:** `https://amazonaws.com`

### 3. Recurso
* `/registra-pedidos`

### 4. Request

```json
{
    "LimitePedidos": 1
}
```

### 4. Response
* status 200 Con el mensaje, que indica la cantidad de pedidos procesados

```json
{
    "status": 200,
    "errorMensaje": null,
    "mensaje": "No hay mensajes para procesar",
    "success": true,
    "body": null
}
```
### 6. Procedimiento almacenado

* El procedimiento se encuentra en la MXBDAJE y es ejecutado desde AWS, recibe los parámetros necesario para registrar el pedidos en la BD
    * `[dbo].[USP_CM_EDI_ALMACENA_JSON_PEDIDO_MX]`
    * `@P_CADENA VARCHAR(50),`
    * `@P_FOLIO VARCHAR(15),`
    * `@P_PEDIDOJSON NVARCHAR(MAX),`
    * `@P_PEDIDOJSONAJE NVARCHAR(MAX),`
    * `@P_PEDIDOEDI NVARCHAR(MAX),`
    * `@P_RESP varchar(12) output`

**Parámetros:**

* **@P_CADENA VARCHAR(50)** - Nombre de la cadena
* **@P_FOLIO VARCHAR(15)** - Numero de la Orden de Compra
* **@P_PEDIDOJSON NVARCHAR(MAX)** - Pedido json que envia el proveedor de facturacion
* **@P_PEDIDOJSONAJE NVARCHAR(MAX)** - Pedido json con ajustes de AJE
* **@P_PEDIDOEDI NVARCHAR(MAX)** - No se utiliza
* **@P_RESP varchar(12) output** - Variable con el resultado de salida
    * **@P_RESP = 0** - proceso exitoso

### Datos de prueba para ejecución de SP

```sql
declare @P_RESP varchar(12)

exec USP_CM_EDI_ALMACENA_JSON_PEDIDO_MX
'NUEVA WAL MART DE MEXICO',
'4477946989'
```
```json
{
  "OrdenCompra": {
    "emisorEdi": null,
    "tipoEdi": null,
    "folioOrdenCompra": "4477946989",
    "glnTienda": "",
    "nombreTienda": "",
    "numeroTienda": "",
    "numeroProveedor": "285422952",
    "fecha": "2025-05-07T00:00:00",
    "fechaCancelacion": "2025-05-12T00:00:00",
    "nombreCliente": "NUEVA WAL MART DE MEXICO",
    "nombreProveedor": "AJEMEX",
    "cadena": "",
    "archivoOrigen": null,
    "items": [
      {
        "codigoBarras": "",
        "codigoCliente": "009584382",
        "precioUnitario": "17.1",
        "unidadMedida": "EA",
        "cantidad": "360",
        "codigoProveedor": "NACIONAL"
      },
      {
        "codigoBarras": "",
        "codigoCliente": "100242385",
        "precioUnitario": "22.96",
        "unidadMedida": "EA",
        "cantidad": "2520",
        "codigoProveedor": "598901"
      }
    ]
  }
},
{
  "OrdenCompra": {
    "emisorEdi": "925485MX00",
    "tipoEdi": "ORDERS",
    "folioOrdenCompra": "1283071434",
    "glnTienda": "7507003120306",
    "nombreTienda": "DISTRIBUTION CENTER 7459",
    "numeroTienda": "",
    "numeroProveedor": "285422950",
    "fecha": "20250507",
    "fechaCancelacion": "20250512",
    "nombreCliente": "",
    "nombreProveedor": "AJEMEX SA DE CV",
    "cadena": "BODEGA",
    "archivoOrigen": "",
    "items": [
      {
        "codigoBarras": "7506495005085",
        "codigoCliente": "100462735",
        "precioUnitario": "5.16",
        "unidadMedida": "EA",
        "cantidad": "864",
        "codigoProveedor": ""
      },
      {
        "codigoBarras": "7506495005108",
        "codigoCliente": "100462738",
        "precioUnitario": "5.16",
        "unidadMedida": "EA",
        "cantidad": "864",
        "codigoProveedor": ""
      },
      {
        "codigoBarras": "7506495005061",
        "codigoCliente": "100462743",
        "precioUnitario": "5.16",
        "unidadMedida": "EA",
        "cantidad": "864",
        "codigoProveedor": ""
      },
      {
        "codigoBarras": "7503027753636",
        "codigoCliente": "101270556",
        "precioUnitario": "6.7833",
        "unidadMedida": "EA",
        "cantidad": "696",
        "codigoProveedor": ""
      }
    ]
  }
},
null,
@P_RESP output

select @p_resp
```

## 2. Procesamiento de pedidos

* Posterior al paso 1, se ejecuta mediante un job en la MXBDAJE el stored procedure: **USP_CM_TRANSFER_MAIN** el cual no recibe parámetros y no tiene una respuesta definida.
* **USP_CM_TRANSFER_MAIN** es el sp que orquesta el registro de los pedidos en magic.
