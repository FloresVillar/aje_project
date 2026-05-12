### Facturación Electrónica

#### Integración de Facturación electrónica

El API de facturación electrónica es un API REST se encuentra alojada en AWS, y es invocada desde la **MXBDAJE**.

**NOTA:**
* Se Adjunta Collection de Postman **Facturación electrónica**
* Para realizar pruebas con postman los headers se deben enviar respetando mayúsculas y minúsculas. para evitar problemas activar la versión 1 de http en postman

```bash
Request
HTTP version: HTTP/1.x
Select the HTTP version to use for sending the request.
```

#### 1. Generación de tokens

**1. Descripción**
Para poder consumir el resto de los endpoints, es necesario ejecutar primero las peticiones de **Token AWS** y **Token Proveedor FE** para obtener las credenciales de acceso. Revisar los recursos de postman.

**2. Recurso postman**
* Token AWS
* Token Proveedor FE

Una vez obtenidos, se deben incluir obligatoriamente ambos tokens en los *headers* de todas las peticiones subsecuentes de la siguiente manera:

* **Authorization**: `Bearer <token_aws>`
* **AuthorizationExt**: `<token_proveedor_fe>`
#### 2. Timbrado

**1. Descripción**
* Recibe el contenido de una factura en JSON para enviarla a timbrar con el proveedor de FE.
* Este endpoint es invocado desde la **MXBDAJE**.

**2. Ruta Base**
* **DEV**: `https://amazonaws.com`

**3. Recurso**
* `/timbrado`

**4. Recurso postman**
* Timbrado

**5. Request de ejemplo**

```bash
{
    "emisor": {
        "rfc": "AJE010718ET5",
        "razonSocial": "AJEMEX",
        "nombre": "AJEMEX"
    },
    "receptor": {
        "rfc": "CDN0402265GA",
        "razonSocial": "COMERCIALIZADORA Y DISTRIBUIDORA DEL NAYAR",
        "nombre": "COMERCIALIZADORA Y DISTRIBUIDORA DEL NAYAR",
        "email": "",
        "domicilioFiscalReceptor": "63117",
        "cfdiRegimenFiscalReceptor": "601"
    },
    "encabezado": {
        "tipoDocumento": "RecepcionDePagos",
        "fecha": "2026-02-27T11:00:40",
        "folio": "00051619",
        "serie": "CPUE",
        "cfdiusoCFDI": "CP01",
        "folioReferencia": "00300001CPUE00051619TEST"
    }
}
        "regimenFiscalEmisor": "601",
        "moneda": "XXX",
        "subTotal": "0",
        "total": "0",
        "versionCFDI": "4.0",
        "cfdiExportacion": "01",
        "lugarExpedicion": "74160",
        "cuerpos": [
            {
                "renglon": "1",
                "cantidad": "1",
                "cfdiClaveProdServ": "84111506",
                "cfdiClaveUnidad": "ACT",
                "unidad": "ACT",
                "concepto": "Pago",
                "pUnitario": "0",
                "importe": "0",
                "claveProdServ": "84111506",
                "claveUnidad": "ACT",
                "cfdiObjetoImp": "01"
            }
        ],
        "pagos": {
            "TotalRetencionesIVA": "",
            "TotalRetencionesISR": "",
            "TotalRetencionesIEPS": "",
            "TotalTrasladosBaseIVA16": "289026.21",
            "TotalTrasladosImpuestoIVA16": "46244.19",
            "TotalTrasladosBaseIVA8": "",
            "TotalTrasladosImpuestoIVA8": "",
            "TotalTrasladosBaseIVA0": "",
            "TotalTrasladosImpuestoIVA0": "",
            "TotalTrasladosBaseIVAExento": "",
            "MontoTotalPagos": "309331.20",
            "pago20pago": [
                {
                    "pagoFechaPago": "2025-12-26T00:00:00",
                    "pagoFormaDePagoP": "03",
                    "pagoMonedaP": "MXN",
                    "pagoTipoCambioP": "1",
                    "pagoMonto": "309331.20",
                    "pagoNumOperacion": "",
                    "pagoRfcEmisorCtaOrd": "",
                    "pagoNomBancoOrdExt": "",
                    "pagoCtaOrdenante": "",
                    "pagoRfcEmisorCtaBen": "",
                    "pagoCtaBeneficiario": "",
                    "pagoTipoCadPago": "",
                    "pagoCertPago": "",
                    "pagoCadPago": "",
                    "pagoSelloPago": "",
                    "pago20doctoRel": [
                        {
                            "codigoMultipleRel": "1",
                            "pagoIdDocumento": "A73EC0E1-C130-4EFA-A451-9B9D2C5181BA",
                            "pagoSerie": "FCCP",
                            "pagoFolio": "00006411",
                            "pagoMonedaDR": "MXN",
                            "EquivalenciaDR": "1",
                            "pagoNumParcialidad": "1",
                            "pagoImpSaldoAnt": "335270.40",
                            "pagoImpPagado": "309331.20",
                            "pagoImpSaldoInsoluto": "25939.2",
                            "ObjetoImpDR": "02",
                            "trasladosDR": [
                                {
                                    "baseDR": "289026.21",
                                    "impuestoDR": "002",
                                    "tipoFactorDR": "Tasa",
                                    "tasaOCuotaDR": "0.160000",
                                    "importeDR": "46244.19"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
                                }
                            ]
                        }
                    ]
                },
                "trasladosP": [
                    {
                        "baseP": "289026.21",
                        "impuestoP": "002",
                        "tipoFactorP": "Tasa",
                        "tasaOCuotaP": "0.160000",
                        "importeP": "46244.19"
                    }
                ]
            }
        ]
    }
}
#### 4. Response
* **status 200**: Con la respuesta de timbrado si el proceso fue exitoso.

```bash
{
    "model": {
        "cfdiXml": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZ3UraA9Inv0Zl04Ij8+PGNmZ...",
        "cfdiInfo": {
            "id": 38139,
            "uuid": "9cbda531-c3ed-438f-81f5-1afa050679b2",
            "fechaTimbrado": "2026-02-27T11:35:55",
            "rfcEmisor": "AJE010718ET5",
            "rfcReceptor": "CDN0402265GA",
            "folio": "00051619",
            "serie": "CPUE",
            "tipoDocumento": "RecepcionDePagos",
            "folioReferencia": "00300001CPUE00051619TEST"
        }
    }
}
            "folioReferencia": "00300001CPUE00051619TEST"
        },
        "cadenaOriginal": "||4.0|CPUE|00051619|2026-02-27T11:00:40|20001000000200001428|0|XXX|0|P|01|74160|AJE010718ET5|AJEMEX|601|CDN0402265GA|COMERCIALIZADORA Y DISTRIBUIDORA DEL NAYAR|63117|601|CP01|84111506|1|ACT|Pago|0|0|01|2.0|289026.21|46244.19|309331.20|2025-12-26T12:00:00|03|MXN|1|309331.20|A73EC0E1-C130-4EFA-A451-9B9D2C5181BA|FCCP|00006411|MXN|1|1|335270.40|309331.20|25939.2|02|289026.21|002|Tasa|0.160000|46244.19|289026.21|002|Tasa|0.160000|46244.19||",
        "cadenaOriginalTimbre": "||1.1|9CBDA531-C3ED-438F-81F5-1AFA050679B2|2026-02-27T11:35:55|INT020124V62|DhuiopiEAOvifSAEIEdmOnpnc5JOUC9APMpapZFZrkQ7kNTpALaUcq7xA+hqtmiS6J1JSlxzNyg8JIGpsuq80YM0PjGv2ZvB6RdMpTdS8oz5Kb0FXN6K0PKYaG1lan9PvOCflm8BVfag0mC9LHK5iMFvQjvAAy+u46ZiHvrWCM8=|30001000000400002495||",
        "links": [
            {
                "rel": "self",
                "href": "https://origon.cloud",
                "action": "GET",
                "types": [
                    "application/json"
                ]
            },
            {
                "rel": "pdf",
                "href": "https://origon.cloud",
                "action": "GET",
                "types": [
                    "application/pdf"
                ]
            }
        ]
    },
    "message": "Solicitud ejecutada con éxito",
    "hasError": false,
    "errorMessage": null,
    "requestId": "8b6d82cd-531b-49fa-b3de-380d5348404b"
}


#### 5. Procedimiento almacenado

* El endpoint no ejecuta ningún Stored Procedure.
* Procedimientos relacionados que invocan el endpoint del timbrado en la **MXBDAJE**:
    * `COM_FACTURA_ELECTRONICA_API_AWS_INTERFAC`
    * `COM_FACTURA_ELECTRONICA_TOKEN_MX`
    * `SP_API_GENERICA`
    * `COM_PROCEXTERNOS_MX`
    * `COM_FACTURA_ELECTRONICA_COMP_PAGOS_AXC_MX`
    * `COM_FACTURA_ELECTRONICA_COMP_PAGOS_MIXTO_MX`
    * `COM_FACTURA_ELECTRONICA_COMP_PAGOS_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_CASA_LEY_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_CHEDRAUI_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_CITY_FRESCO_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_ELDUERO_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_HEB_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_OPE_MERCO_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_OXXO_MX`
    * `COM_FACTURA_ELECTRONICA_ADD_SORIANA_MX`
    * `COM_FACTURA_ELECTRONICA_CERILLERA_MX`
    * `COM_FACTURA_ELECTRONICA_CONTADO_MX`
    * `COM_FACTURA_ELECTRONICA_ESTANDAR_MX`
    * `COM_FACTURA_ELECTRONICA_EXPORTACION_MX`
    * `COM_FACTURA_ELECTRONICA_NCC_ESTANDAR_MX`
    * `COM_FACTURA_ELECTRONICA_NCC_EXPORTACION_MX`

#### 3. Descarga Documento PDF

**1. Descripción**
* Descarga del api de aws las facturas en formato PDF.
* Este endpoint es invocado desde las terminales de magic mediante una aplicación java que se ejecuta en consola.

**2. Ruta Base**
* **DEV**: `https://amazonaws.com`

**3. Recurso**
* `/descargar-doc`

**4. Recurso postman**
* Descarga Doc PDF

**5. Request de ejemplo**

```json
{
    "fileName": "AJE010718ET5_GZA9104307K6_CPUE_00044417_20250110",
    "docType": "pdf",
    "fxcType": "RecepcionDePagos",
    "fxcId": 1283754
}
```

#### 4. Response
* **status 200**: Con el documento en base64

```json
{
    "status": 200,
    "errorMessage": null,
    "mensaje": "Documento PDF obtenido",
    "success": true,
    "body": {
        "filename": "Facturas/2025/1/AJE010718ET5_GZA9104307K6_CPUE_00044417_20250110.pdf",
        "documento": "JVBERi0xLjQKJel_jz9MKMSAwIG9iajw8L0luRGF0ZSHEOjImMjuwMTEwMTkx..."
    }
}
```

[Página] 4 de 13
#### 4. Solicitud Cancelación

**1. Descripción**
* Recurso para enviar a cancelar alguna factura a la entidad fiscal SAT.
* Este endpoint es invocado desde la **MXBDAJE**.
* No se tiene habilitado con el proveedor la cancelación en ambiente **DEV**.

**2. Ruta Base**
* **DEV**: `https://amazonaws.com`

**3. Recurso**
* `/cancelacion`

**4. Recurso postman**
* Solicitud Cancelación

**5. Request de ejemplo**

```json
{
    "uuid": "b8ab0f0c-daca-498b-a182-db2d9dfd3f28",
    "tipoDocumento": "Factura",
    "user": "TEST",
    "deleteFolio": false,
    "reason": "02",
    "substitutionFolio": ""
}
```

**4. Response**
* **status 200**: Con los detalles de la cancelación.

```json
{
    "statusCode": 200,
    "errorMensaje": null,
    "mensajeResp": "En proceso",
    "success": true,
    "body": {
        "model": {
            "uuid": "9cbda531-c3ed-438f-81f5-1afa050679b2",
            "queryCancellationId": "fba86378-3124-4f9a-b578-eeee48416568",
            "isSucessRequest": true,
            "message": "Se realizó la solicitud de cancelación correctamente"
        },
        "message": "Solicitud procesada con éxito.",
        "hasError": false,
        "errorMessage": null,
        "requestId": "b16276db-b6cd-4fb2-b992-7fcf83713541"
    }
}
```

**5. Procedimiento almacenado**
* Este recurso no ejecuta ningún Stored Procedure.
* Procedimientos relacionados que invocan el endpoint de la cancelación en la **MXBDAJE**:
    * `COM_FACTURA_ELECTRONICA_API_AWS_INTERFAC`
    * `COM_FACTURA_ELECTRONICA_TOKEN_MX`
    * `SP_API_GENERICA`
    * `USP_FEX_CFDI_CAN_MANDA_CANCELAR_CPG`
    * `USP_FEX_CFDI_CAN_MANDA_LISTA_A_CANCELAR`
#### 5. Consulta de Cancelación

**1. Descripción**
* Recurso para enviar a cancelar alguna factura a la entidad fiscal SAT.
* Este endpoint es invocado desde la **MXBDAJE**.
* No se tiene habilitado con el proveedor la cancelación en ambiente **DEV**.

**2. Ruta Base**
* **DEV**: `https://amazonaws.com`

**3. Recurso**
* `/consulta-cancelacion`

**4. Recurso postman**
* Consulta Cancelación

**5. Request de ejemplo**

```json
{
    "uuid": "b8ab0f0c-daca-498b-a182-db2d9dfd3f28",
    "id": "",
    "tipoDocumento": "Factura"
}
```

**4. Response**
* **status 200**: Con los detalles de la cancelación.

```json
{
    "statusCode": 200,
    "errorMensaje": null,
    "mensajeResp": "En proceso",
    "success": true,
    "body": {
        "model": {
            "queryCancellationId": "39ed9024-0171-4701-b956-2df9be60339a",
            "status": "Cancelado",
            "statusDesc": "Cancelado sin aceptación",
            "date": "2026-03-12T12:46:24.217",
            "error": null,
            "events": [
                {
                    "queryCancellationId": "39ed9024-0171-4701-b956-2df9be60339a",
                    "acuse": "<?xml version=\"1.0\"?>\r\n<Acuse xmlns:xsd=\"http://w3.org\" xmlns:xsi=\"http://w3.org-instance\">\r\n <ExtensionData />\r\n <CodigoEstatus>S - Comprobante obtenido satisfactoriamente.</CodigoEstatus>\r\n <EsCancelable>No Cancelable</EsCancelable>\r\n <Estado>Cancelado</Estado>\r\n <EstatusCancelacion>Cancelado sin aceptación</EstatusCancelacion>\r\n</Acuse>",
                    "date": "2026-03-12T12:46:24.217"
                }
            ]
        },
        "message": "Solicitud ejecutada con éxito.",
        "hasError": false,
        "errorMessage": null,
        "requestId": "01afbbb9-9926-465c-ba8b-b52a4057839c"
    }
}
```
 

* Este recurso no ejecuta ningún Stored Procedure.
* Procedimientos relacionados que invocan el endpoint del cancelación en la MXBDAJE:
    * COM_FACTURA_ELECTRONICA_API_AWS_INTERFAC
    * COM_FACTURA_ELECTRONICA_TOKEN_MX
    * SP_API_GENERICA
    * USP_FEX_CFDI_CAN_CONSULTA_Y_ACT_ESTATUS
    * USP_FEX_CFDI_CAN_REG_ACUSE_ANULACION_CPG
    * USP_FEX_CFDI_CAN_REG_ACUSE_ANULACION

---

#### 6. Consulta de Cancelación

##### 1. Descripción
* Recurso para enviar a cancelar alguna factura a la entidad fiscal SAT.
* Este endpoint es invocado desde la MXBDAJE.
* No se tiene habilitado con el proveedor la cancelación en ambiente DEV.

##### 2. Ruta Base
* DEV: https://h6hkk0gt1f.execute-api.us-east-2.amazonaws.com/dev

##### 3. Recurso
* /consulta-cancelacion

##### 4. Recurso postman
* Consulta Cancelación

##### 5. Request de ejemplo
{
    "uuid": "b8ab0f0c-daca-498b-a182-db2d9dfd3f28",
    "id": "",
    "tipoDocumento": "Factura"
}

##### 4. Response
* status 200 Con los detalles de la cancelación.

---

##### 5. Procedimiento almacenado (Repetición en documento)

* Este recurso no ejecuta ningún Stored Procedure.
* Procedimientos relacionados que invocan el endpoint del cancelación en la MXBDAJE:
    * COM_FACTURA_ELECTRONICA_API_AWS_INTERFAC
    * COM_FACTURA_ELECTRONICA_TOKEN_MX
    * SP_API_GENERICA
    * USP_FEX_CFDI_CAN_CONSULTA_Y_ACT_ESTATUS
    * USP_FEX_CFDI_CAN_REG_ACUSE_ANULACION_CPG
    * USP_FEX_CFDI_CAN_REG_ACUSE_ANULACION

#### 7. Genera Json Factura

###### 1. Descripción
* Recurso para generar en json de cualquier factura, y pueda ser editado o ajustado antes de su timbrado.

###### 2. Ruta Base
* **DEV:** https://h6hkk0gt1f.execute-api.us-east-2.amazonaws.com/dev

###### 3. Recurso
* /json

###### 4. Recurso postman
* Genera Json Factura

###### 5. Request de ejemplo
{
    "compania": "0030",
    "sucursal": "21",
    "emisor": "02",
    "tipoDocu": "FXC",
    "nroDocu": 500913
}

###### 4. Response
* **status 200** Con el json de la factura.

```json
{
  "status": 200,
  "errorMensaje": "",
  "mensaje": "Json obtenido correctamente",
  "success": true,
  "body": {
    "emisor": {
      "rfc": "AJE010718ET5",
      "razonSocial": "AJEMEX",
      "domicilio": {
        "calle": "CA. CALLE MANZANA ALOTE7",
        "pais": "MEXICO",
        "codigoPostal": "74160",
        "noExterior": "LOTE7",
        "noInterior": "",
        "colonia": "PARQUE INDUSTRIAL SAN MIGUEL",
        "localidad": "SAN MIGUEL TIANGUIZOLCO",
        "referencia": "",
        "municipio": "HUEJOTZINGO",
        "telefono": "0",
        "estado": "PUEBLA"
      },
      "sucursal": {
        "calle": "CA. CALLE 23365 ",
        "noExterior": " 365",
        "noInterior": "",
        "colonia": " PASEOS DE ITZINCAB",
        "localidad": "PASEOS DE ITZINCAB",
        "referencia": "",
        "municipio": "MERIDA",
        "estado": "YUCATAN",
        "pais": "MEXICO",
        "codigoPostal": "97390",
        "telefono": ""
      }
    },
    "receptor": {
      "rfc": "XAXX010101000",
      "razonSocial": "PUBLICO EN GENERAL",
      "cfdiusoCFDI": "S01",
      "email": "facturacion.electronica.mx@ajegroup.com",
      "domicilioFiscalReceptor": "97390",
      "regimenFiscalReceptor": "616",
      "domicilio": {
        "calle": "CALLE 23 #365 X46 Y 50",
        "municipio": "MERIDA",
        "estado": "YUCATAN",
        "codigoPostal": "97390",
        "noExterior": "365",
        "noInterior": "",
        "colonia": "ITZINCAB",
        "localidad": "XOCLAN XBECH",
        "referencia": "XOCLAN XBECH",
        "pais": "MEXICO"
      }
    },
    "encabezado": {
      "cuenta": "",
      "nombreCorto": "FA",
      "tipoDocumento": "Factura",
      "FolioReferencia": "00302102FXCFMED00197730",
      "folio": "00197730",
      "serie": "FMED",
      "tipoCambio": "",
      "lugarExpedicion": {
        "codigoPostal": "97390"
      },
      "formaPago": "01",
      "metodoPago": "PUE",
      "regimenFiscalEmisor": "601",
      "moneda": "MXN",
      "subTotal": "13915.41",
      "iva": "1968.16",
      "montoDescuento": "1392.71",
      "total": "14490.86",
      "fecha": "2026-03-06T14:41:22",
      "versionCFDI": "4.0",
      "cfdiExportacion": "01",
      "tienda": {
        "eanTienda": "",
        "noTienda": "",
        "nombreTienda": "",
        "domicilio": {
          "calle": "CA. CALLE 23 #365 X46 Y 50",
          "noExterior": "365",
          "colonia": "ITZINCAB",
          "municipio": "MERIDA",
          "estado": "YUCATAN",
          "codigoPostal": "97246",
          "noInterior": "",
          "localidad": "XOCLAN XBECH",
          "referencia": "",
          "pais": "MEXICO"
        }
      },
      "notas": [
        "GUIA..: JMED-0000774498 CLIENTE : 1795257 SUC.: MERIDA OC:"
      ],
      "cuerpos": [
        {
          "renglon": "1",
          "concepto": "Venta",
          "cantidad": "1",
          "claveUnidad": "ACT",
          "precioUnitario": "358.62",
          "preciobase": "179.31",
          "importe": "358.62",
          "claveProdServ": "01010101",
          "precioUnitarioSinDescuento": "208.00",
          "ivaPct": "0.16",
          "ivaMonto": "57.38",
          "iepsPct": "0",
          "iepsMonto": "0.00",
          "codigoBarras": "7750670000604",
          "precioUnitarioConImpuesto": "208.00",
          "importeConImpuesto": "416.00",
          "cfdiObjetoImp": "02",
          "traslados": [
            {
              "base": "358.63",
              "importe": "57.38",
              "impuesto": "002",
              "tipoFactor": "Tasa",
              "tasaOCuota": "0.16"
            }
          ],
          "retenciones": []
        }
      ],
      "informacionGlobal": {
        "periodicidad": "01",
        "meses": "03",
        "año": "2025"
      },
      "impuestos": [
        {
          "totalImpuestosTrasladados": 1968.16,
          "totalImpuestosRetenidos": 0,
          "traslados": [
            {
              "impuesto": "002",
              "importe": "1968.16",
              "tasaOCuota": "0.16",
              "tipoFactor": "Tasa",
              "cfdiBase": "12301.01"
            },
            {
              "impuesto": "002",
              "importe": "0.00",
              "tasaOCuota": "0",
              "tipoFactor": "Tasa",
              "cfdiBase": "235.00"
            }
          ],
          "retenciones": []
        }
      ]
    }
  }
}
```
#### 8. Genera Json Pago

##### 1. Descripción

- Recurso para generar en json de de cualquier complemento de pago, y pueda ser editado o ajustado antes de su timbrado.

##### 2. Ruta Base

```bash
DEV: https://h6hkk0gt1f.execute-api.us-east-2.amazonaws.com/dev
```

##### 3. Recursos

```bash
/pagos/json
```

##### 4. Recurso postman

- Genera Json Pago

##### 5. Request de ejemplo

```bash
{
    "tipoPago":"",
    "compania":"0030",
    "sucursal":"0001",
    "transaccion":"BIG",
    "transmov":"BDB",
    "nroDocu":"1555429118107",
    "fechaEmision":"733909"
}
```

##### 4. Response

- status 200 Con el json de la factura.

```bash
{
  "status": 200,
  "errorMensaje": "",
  "mensaje": "Json obtenido correctamente",
  "success": true,
  "body": {
    "emisor": {
      "rfc": "AJE010718ET5",
      "razonSocial": "AJEMEX",
      "nombre": "AJEMEX"
    },
    "receptor": {
      "rfc": "IVE210223TA5",
      "razonSocial": "INFINITO VERDE",
      "nombre": "INFINITO VERDE",
      "email": "",
      "domicilioFiscalReceptor": "64040",
      "cfdiRegimenFiscalReceptor": "601"
    },
    "encabezado": {
      "tipoDocumento": "RecepcionDePagos",
      "fecha": "2026-03-06T14:55:30",
      "folio": "00045278",
      "serie": "CPUE",
      "cfdiusoCFDI": "CP01",
      "folioReferencia": "00300001CPUE00045278",
      "regimenFiscalEmisor": "601",
      "moneda": "XXX",
      "subTotal": "0",
      "total": "0",
      "versionCFDI": "4.0",
      "cfdiExportacion": "01",
      "lugarExpedicion": "74160",
      "cuerpos": [
        {
          "renglon": "1",
          "cantidad": "1",
          "cfdiClaveProdServ": "84111506",
          "cfdiClaveUnidad": "ACT",
          "unidad": "ACT",
          "concepto": "Pago",
          "pUnitario": "0",
          "importe": "0",
          "claveProdServ": "84111506",
          "claveUnidad": "ACT",
          "cfdiObjetoImp": "01"
        }
      ],
      "pagos": {
        "TotalRetencionesIVA": "2897.25",
        "TotalRetencionesISR": "",
        "TotalRetencionesIEPS": "",
        "TotalTrasladosBaseIVA16": "18107.81",
        "TotalTrasladosImpuestoIVA16": "2897.25",
        "TotalTrasladosBaseIVA8": "",
        "TotalTrasladosImpuestoIVA8": "",
        "TotalTrasladosBaseIVA0": "",
        "TotalTrasladosImpuestoIVA0": "",
        "TotalTrasladosBaseIVAExento": "",
        "MontoTotalPagos": "18107.80",
        "pago20pago": [
          {
            "pagoFechaPago": "2025-02-27T00:00:00",
            "pagoFormaDePagoP": "03",
            "pagoMonedaP": "MXN",
            "pagoTipoCambioP": "1",
            "pagoMonto": "18107.80",
            "pagoNumOperacion": "",
            "pagoRfcEmisorCtaOrd": "",
            "pagoNomBancoOrdExt": "",
            "pagoCtaOrdenante": "",
            "pagoRfcEmisorCtaBen": "",
            "pagoCtaBeneficiario": "",
            "pagoTipoCadPago": "",
            "pagoCertPago": "",
            "pagoCadPago": "",
            "pagoSelloPago": "",
            "pago20doctoRel": [
              {
                "codigoMultipleRel": "1",
                "pagoIdDocumento": "B82109A3-CED4-40E6-A0AE-39CFF276E976",
                "pagoSerie": "MT15",
                "pagoFolio": "00000058",
                "pagoMonedaDR": "MXN",
                "EquivalenciaDR": "1",
                "pagoNumParcialidad": "1",
                "pagoImpSaldoAnt": "18107.80",
                "pagoImpPagado": "18107.80",
                "pagoImpSaldoInsoluto": "0.00",
                "ObjetoImpDR": "02",
                "trasladosDR": [
                  {
                    "baseDR": "18107.81",
                    "impuestoDR": "002",
                    "tipoFactorDR": "Tasa",
                    "tasaOCuotaDR": "0.160000",
                    "importeDR": "2897.25"
                  }
                ],
                "retencionesDR": [
                  {
                    "baseDR": "18107.81",
                    "impuestoDR": "002",
                    "tipoFactorDR": "Tasa",
                    "tasaOCuotaDR": "0.160000",
                    "importeDR": "2897.25"
                  }
                ]
              }
            ],
            "trasladosP": [
              {
                "baseP": "18107.81",
                "impuestoP": "002",
                "tipoFactorP": "Tasa",
                "tasaOCuotaP": "0.160000",
                "ImporteP": "2897.25"
              }
            ],
            "retencionesP": [
              {
                "impuestoP": "002",
                "ImporteP": "2897.25"
              }
            ]
          }
        ]
      }
    }
  }
}
```

##### 5. Procedimiento almacenado

- El endpoint ejecuta el siguientes stored procedure en la MXBDAJE:

```bash
COM_FACTURA_ELECTRONICA_COMP_PAGOS_AXC_MX
COM_FACTURA_ELECTRONICA_COMP_PAGOS_MIXTO_MX
COM_FACTURA_ELECTRONICA_COMP_PAGOS_MX
```

#### 9. Retimbra Json Factura

##### 1. Descripción

- Recurso para enviar a timbrar el json de alguna factura y actualice la respuesta en la MXBDAJE

##### 2. Ruta Base

```bash
DEV: https://h6hkk0gt1f.execute-api.us-east-2.amazonaws.com/dev
```

##### 3. Recurso

```bash
/retimbra-json
```

##### 4. Recurso postman

- Retimbra Json Factura

##### 5. Request de ejemplo

```bash
{
    "compania":"0030",
    "sucursal":"21",
    "emisor":"02",
    "tipoDocu":"FXC",
    "nroDocu":"501341",
    "json": {

    }
}
```

##### 6. Response

- status 200 Con la respuesta de timbrado.

##### 7. Procedimiento almacenado

- El endpoint ejecuta el siguientes stored procedure en la MXBDAJE:

```bash
FE_TIMBRA_JSON
```

#### 10. Retimbra Json Pago

##### 1. Descripción

- Recurso para enviar a timbrar el json de alguna factura de complemento de pago y actualice la respuesta en la MXBDAJE

##### 2. Ruta Base

```bash
DEV: https://h6hkk0gt1f.execute-api.us-east-2.amazonaws.com/dev
```

##### 3. Recursos

```bash
/pagos/retimbra
```

##### 4. Recurso postman

- Retimbra Json Pago


##### 5. Request de ejemplo

```bash
{
    "compania": "0030",
    "sucursal": "0001",
    "transaccion": "AXC",
    "transmov": "AXC",
    "nroDocu": "138911",
    "fechaEmision": 739220,
    "json": {
        "emisor": {
            ...
        }
    }
}
```

##### 6. Response

- status 200 Con la respuesta de timbrado.

##### 7. Procedimiento almacenado

- El endpoint ejecuta el siguientes stored procedure en la MXBDAJE:

```bash
PAGOS_TIMBRA_JSON
```