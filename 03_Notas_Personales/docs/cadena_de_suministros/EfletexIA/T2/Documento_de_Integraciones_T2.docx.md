#### Documento de Integraciones T2.docx

**DOCUMENTACIÓN:** Efletexia T2 Documento de especificaciones del proyecto  
**País:** GLOBAL  
**Autor:** Wilder Zevallos Quevedo  
**Revisado por:** Wendy Villegas  
**Fecha:** 06 marzo 2026.

---

**Contenido**

1. **LISTA DE INTEGRACIONES** 3
2. **DETALLE DE INTEGRACIONES** 3
    - 2.1. **LOGIN** 3
    - 2.2. **PEDIDOS** 3
    - 2.3. **CLIENTES** 5
    - 2.4. **RUTAS PLANIFICADAS** 7

---

##### 1 **LISTA DE INTEGRACIONES**

Estos son las funciones encontradas en AWS Lambda de la cadena de desarrollo:


| INTEGRACIÓN | ENDPOINT | STORE PROCEDURE |
| :--- | :--- | :--- |
| LOGIN | https://ldxxck4te1.execute-api.us-east-2.amazonaws.com/dev/login | COM_PLINT_CONSUMO_AWS |
| PEDIDOS | https://ldxxck4te1.execute-api.us-east-2.amazonaws.com/dev/pedidos | COM_PREPARAR_CARGA_PEDIDO_PLINT |
| CLIENTES | https://ldxxck4te1.execute-api.us-east-2.amazonaws.com/dev/maestros | COM_PREPARAR_CARGA_PEDIDO_PLINT |
| PEDIDOS PLANIFICADOS | https://ldxxck4te1.execute-api.us-east-2.amazonaws.com/dev/pedidos-planificados | COM_PLINT_CONSULTA_PEDIDO_AWS |

---

##### 2 **DETALLE DE INTEGRACIONES**

###### 2.1. **LOGIN**

**Objetivo:**
Conseguir el token del usuario y contraseña enviados en formato JSON dentro del BODY de la invocación. Las propiedades dentro del JSON son:


| PROPIEDAD | TIPO | DESCRIPCIÓN | VALOR / EJEMPLO |
| :--- | :--- | :--- | :--- |
| usuario | String | Usuario de Cognito | efletexservices |
| clave | String | Contraseña de cognito | *********** |

###### 2.2. **PEDIDOS**

**Objetivo:**
Enviar la información de los pedidos del día por sucursal en formato XML dentro del BODY.

Las propiedades dentro del XML de la integración son:


| PROPIEDAD | TIPO | DESCRIPCIÓN | VALOR / EJEMPLO |
| :--- | :--- | :--- | :--- |
| compania | String | Codigo de compañía | 0009 |
| Sucursal | String | Codigo de sucursal | 57 |

[Página] 3


| idTableBM | String | ID de la tabla de integraciones | 560483 |
| pedido | xml | Lista de pedidos | Detalles en la siguiente tabla |

**Estructura de "pedido":**


| PROPIEDAD | TIPO | DESCRIPCIÓN | EJEMPLO |
| :--- | :--- | :--- | :--- |
| ID | String | Identificador del pedido Origen de documento + "-" + Numero de pedido + "-" + Codigo de Cliente | 200-34403-18609 |
| clienteID | Integer | Codigo de Cliente | 18609 |
| cajas | Decimal | Cantidad total de cajas del pedido | 1.0000000000000000e+000 |
| peso | Decimal | Peso total de las cajas del pedido | 9.6400000000000001e+000 |
| volumen | Decimal | Volumen total de las cajas del pedido | 9.0000000000000000e+000 |
| fechaEnvio | String | Fecha de entrega | 2026-03-06 |
| pedidoDetalle | xml | Detalle del pedido | Detalles en la siguiente tabla |

**Estructura de "pedidoDetalle":**


| PROPIEDAD | TIPO | DESCRIPCIÓN | EJEMPLO |
| :--- | :--- | :--- | :--- |
| articuloID | Integer | Codigo de artículo | 621790 |
| articuloDescripcion | String | Descripción del artículo | SPORADE TROPICAL PET NO RETORNABLE 1500 ML 6 MC |
| cajas | Integer | Cantidad de cajas | 1 |
| unidades | Integer | Cantidad de unidades | 0 |
| pesoTotal | Decimal | Peso total de cajas y unidades | 9.64 |
| volumenTotal | Decimal | Volumen total de cajas y unidades | 9 |
| peso | Decimal | Peso por caja | 9.64 |
| volumen | Decimal | Volumen por caja | 9 |
| procedimientoDescripcion | String | Descripción del procedimiento | Venta |
| qContenido | Integer | Cantidad de botellas por caja | 6 |

[Página] 4


| totalBotellas | Integer | Cantidad de botellas | 6 |
| codPromocion | Integer | Codigo de promoción | 0 |

**Ejemplo del XML:**
```xml
<pedidos>
    <compania>1003</compania>
    <sucursal>14</sucursal>
    <idTableBM>560186</idTableBM>
    <pedido>
        <ID>200-27947-68452</ID>
        <clienteID>68452</clienteID>
        <cajas>6</cajas>
        <peso>14.22</peso>
        <volumen>12.78</volumen>
        <tipoPedido>Venta</tipoPedido>
        <fechaEnvio>2026-03-06</fechaEnvio>
        <pedidoDetalle>
            <articuloID>624048</articuloID>
            <articuloDescripcion>KR KOLITA LATA 355 ML 6 MC</articuloDescripcion>
            <cajas>6</cajas>
            <unidades>0</unidades>
            <pesoTotal>14.22</pesoTotal>
            <volumenTotal>12.78</volumenTotal>
            <peso>14.22</peso>
            <volumen>12.78</volumen>
            <procedimientoDescripcion>Venta</procedimientoDescripcion>
            <qContenido>6</qContenido>
            <totalBotellas>36</totalBotellas>
            <codPromocion>17085</codPromocion>
        </pedidoDetalle>
    </pedido>
</pedidos>
```

###### 2.3. **CLIENTES**

**Objetivo:**
Enviar la información de los clientes en formato XML dentro del BODY.

Las propiedades dentro del XML de la integración son:

[Página] 5


| PROPIEDAD | TIPO | DESCRIPCIÓN | VALOR / EJEMPLO |
| :--- | :--- | :--- | :--- |
| compania | String | Codigo de compañía | 0009 |
| Sucursal | String | Codigo de sucursal | 57 |
| Tipo | String | Identificador del tipo de integración | Siempre es "CLIENTES" |
| cliente | xml | Propiedad que se puede repetir por la cantidad de clientes. | Detalles en la siguiente tabla |

**Estructura de "cliente":**


| PROPIEDAD | TIPO | DESCRIPCIÓN | EJEMPLO |
| :--- | :--- | :--- | :--- |
| clienteID | Integer | Codigo de Cliente | 18609 |
| codigo_compania | String | Codigo de compañía | 1003 |
| codigo_region | String | Codigo de región | 05 |
| codigo_sucursal | String | Codigo de sucursal | 01 |
| zonaID | Integer | Zona del cliente | 1682 |
| rutaID | Integer | Ruta del cliente | 13420 |
| moduloID | Integer | Módulo del cliente | 94814 |
| nombre | String | Codigo de forma de pago | HEINEKEN PERU S.A.C. |
| direccion | String | Dirección del cliente | ZI SANTA MARIA DE HUACHIPA AV LA PAZ Nro. 129 |
| telefono | String | teléfono del cliente | 918456742 |
| RUC | String | RUC del cliente | 20605524126 |
| pais | String | Codigo de país | PE |
| latitude | Decimal | Latitud de ubicación | -12.0163 |
| longitude | Decimal | Longitud de ubicación | -76.9306 |
| diasEnvio | String | Primera letra de los días de envió concatenados | MRJVSD |
| codigoCanal | String | Codigo de Canal | 003 |
| codigoGiro | String | Codigo de Giro | 720 |
| codigoSubGiro | String | Codigo de SubGiro | 721 |
| codigo_lp | String | Codigo de Lista de precio | 13 |
| colonia | String | Colonia o Distrito | LURIGANCHO |
| calle | String | Calle | Calle Las Begonias |
| numero | String | Numero de la casa | 129 |
| unidfiscal | String | Unidad fiscal | 15 |
| tipcliente | String | Tipo de cliente | 001 |

[Página] 6


| PROPIEDAD | TIPO | DESCRIPCIÓN | EJEMPLO |
| :--- | :--- | :--- | :--- |
| procedcli | String | Prrocedimiento de cliente | N |
| formpago | String | Codigo de forma de pago | 004 |

**Ejemplo del XML:**

[Página] 7

**Ejemplo del XML:**
```xml
<maestro>
    <compania>1003</compania>
    <idTableBM>560648</idTableBM>
    <tipo>CLIENTES</tipo>
    <cliente>
        <clienteID>504</clienteID>
        <codigo_compania>1003</codigo_compania>
        <codigo_region />
        <codigo_sucursal>01</codigo_sucursal>
        <zonaID>9655</zonaID>
        <rutaID>93214</rutaID>
        <moduloID>94814</moduloID>
        <nombre>HEINEKEN PERU S.A.C.</nombre>
        <direccion>ZI SANTA MARIA DE HUACHIPA AV LA PAZ Nro. 129</direccion>
        <telefono>0</telefono>
        <RUC>20605524126</RUC>
        <pais>PE</pais>
        <latitude>-12.0163</latitude>
        <longitude>-76.9306</longitude>
        <diasEnvio>MRJVSD</diasEnvio>
        <codigoCanal>003</codigoCanal>
        <codigoGiro>720</codigoGiro>
        <codigoSubGiro>721</codigoSubGiro>
        <codigo_lp>13</codigo_lp>
        <colonia>LURIGANCHO</colonia>
        <calle />
        <numero>129</numero>
        <unidfiscal>15</unidfiscal>
        <tipcliente>001</tipcliente>
        <procedcli>N</procedcli>
        <formpago>004</formpago>
    </cliente>
</maestro>
```

###### 2.4. **RUTAS PLANIFICADAS**

**Objetivo:**
Recibir la información de los pedidos asignados a los vehículos en formato XML dentro del BODY.

[Página] 8

Las propiedades dentro del XML de la integración son:



| PROPIEDAD | TIPO | DESCRIPCIÓN | VALOR / EJEMPLO |
| :--- | :--- | :--- | :--- |
| compania | String | Codigo de compañía | 0009 |
| sucursal | String | Codigo de sucursal | 57 |
| PlanificacionPedido | array | Lista de PlanificacionPedido | Detalles en la siguiente tabla |

**Estructura de "PlanificacionPedido":**



| PROPIEDAD | TIPO | DESCRIPCIÓN | VALOR / EJEMPLO |
| :--- | :--- | :--- | :--- |
| ID | String | Identificador del pedido Origen de documento + "-" + Numero de pedido + "-" + Codigo de Cliente | 200-34403-18609 |
| clienteID | Integer | Codigo de Cliente | 18609 |
| vehiculoID | String | ID de la tabla de integraciones | D00736 |
| secuencia | Integer | Secuencia de la Integración | 40 |
| nviaje | Integer | Numero de viaje | 1 |
| nparticion | Integer | Numero de partición | 1 |
| detalle | array | Lista de detalles | Detalles en la siguiente tabla |

**Estructura de "detalle":**



| PROPIEDAD | TIPO | DESCRIPCIÓN | EJEMPLO |
| :--- | :--- | :--- | :--- |
| articuloID | Integer | Codigo de Cliente | 18609 |
| cajas | Decimal | Cantidad total de cajas del pedido | 2 |

**Ejemplo del XML:**

[Página] 9

<RutaPedidoBody>
    <compania>1003</compania>
    <sucursal>06</sucursal>
    <PlanificacionPedido>
        <PlanificacionPedido>
            <ID>200-135188-24349</ID>
            <clienteID>24349</clienteID>
            <vehiculoID>D00736</vehiculoID>
            <secuencia>40</secuencia>
            <nviaje>1</nviaje>
            <nparticion />
            <detalle>
                <detalle>
                    <articuloID>608469</articuloID>
                    <cajas>2</cajas>
                </detalle>
                <detalle>
                    <articuloID>621790</articuloID>
                    <cajas>1</cajas>
                </detalle>
                <detalle>
                    <articuloID>622420</articuloID>
                    <cajas>1</cajas>
                </detalle>
            </detalle>
        </PlanificacionPedido>
    </PlanificacionPedido>
</RutaPedidoBody>


