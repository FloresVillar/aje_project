## Acceso a aplicacion de recepcion de facturas en Test.docx

Usuario para el ambiente de test.
Recepción de facturas

https://facturaciontest.ajemex.net/
Usuario: miguel.perez.mx
Pass: Qwerty123

## Recepcion de Facturas.postman_collection.json
Revisar el .json 

## Recepcion Facturas Viaticos V1.pdf

### Integración de Recepcion Facturas Viaticos V1
* Se Adjunta Collection de Postman **Recepción de Facturas**

---

#### 1. Obtener Companias (SOAP)

##### 1. Descripción
* Método para obtener la lista de compañías de **AJE Mx**.
* El web service soap recibe la respuesta del stored procedure y la devuelve por su response.

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A
* **Recurso Postman:** Obtener Companias (SOAP)

###### Procedimiento almacenado
* `USP_MAGICERP_SQL_COMPANIAS_MX`
* **Parámetros:** N/A

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:getCompanias"`

**Parámetros:** N/A

**Request Body:**
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:getCompanias/>
   </soap:Body>
</soap:Envelope>
```
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getCompaniasResponse xmlns:ns="http://auth.aje.com">
         <ns:return>
            <data>
               <web-service version="1.0"/>
               <erp id="Magic Software"/>
               <middleware api="jax-ws"/>
               <compania compania="0030" direccion="MANZANA A LOTE 7 PARQUE INDUSTRIAL SAN MIGUEL HUEJOTZINGO PUEBLA C.P 74160" nombre="AJEMEX" rfc="AJE810718ET5"/>
               <compania compania="0032" direccion="MANZANA 'A', LOTE 8 al 12 CORREDOR INDUSTRIAL QUETZALCOATL" nombre="AJEGROUP" rfc="AJE0404238B4"/>
               <compania compania="0033" direccion="MANZANA 'A', LOTES 8 AL 12 CORREDOR INDUSTRIAL QUETZALCOATL, HUEJOTZINGO, PUEBLA" nombre="AJEMEX CONSULTORES" rfc="ACO8112189L6"/>
               <compania compania="0035" direccion="CALLE MANZANA A LOTE 8 AL 12 PARQUE INDUSTRIAL SAN MIGUEL SANTA ANA XALMIMILULCO" nombre="INMOBILIARIA ALPAMAYO" rfc="IAL0411178Z8"/>
               <compania compania="0036" direccion="Calle Cuetzalan 36-Lomas de Angelopolis- San Andres de Cholula" nombre="TACZANA MEXICO S.A. DE C.V." rfc="TME2311076K0"/>
               <compania compania="0060" direccion="MANZANA A LOTE 7 PARQUE INDUSTRIAL SAN MIGUEL HUEJOTZINGO PUEBLA C.P 74160" nombre="COCENTRO" rfc="COC040303775"/>
            </data>
         </ns:return>
      </ns:getCompaniasResponse>
   </soapenv:Body>
</soapenv:Envelope>

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A.
* **Recurso Postmam:** Obtener Detalles de Empleado (SOAP)

###### Procedimiento almacenado
* `USP_MAGICERP_SQL_EMPLEADOS_MX @P_COMPANIA CHAR(4), @P_USUARIO_AD VARCHAR(100)`
* **Parámetros:**
    * `@P_COMPANIA CHAR(4)` – Código de compañía del empleado
    * `@P_USUARIO_AD VARCHAR(100)` – Usuario de AD del empleado a buscar

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:getEmpleados"`

**Parámetros:**
* `compania`: Código de compañía del empleado
* `usuario_AD`: Usuario de AD del empleado a buscar

**Request:**
Los parámetros pasan directo al stored
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:getEmpleados>
         <!--Optional:-->
         <auth:compania>0033</auth:compania>
         <!--Optional:-->
         <auth:usuario_AD>miguel.perez.mx</auth:usuario_AD>
      </auth:getEmpleados>
   </soap:Body>
</soap:Envelope>
```

##### 4. Response
**Response:**
```xml
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getEmpleadosResponse xmlns:ns="http://auth.aje.com">
         <ns:return>
            <data>
               <web-service version="1.0"/>
               <erp id="Magic Software"/>
               <middleware api="jax-ws"/>
               <empleado apellidos="SOLIS PEREZ" area_func="61" ccosto="240010201" compania="0033" correo="miguel.solis.mx@ajegroup.com" empleado="8936" f_nac="1985-08-02" nivel_auth="21" nombre="MIGUEL ANGEL" sexo="M" usuario_ad="miguel.perez.mx"/>
            </data>
         </ns:return>
      </ns:getEmpleadosResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

#### 3. Obtener Detalles de Plan de Viaje (SOAP)

##### 1. Descripción
* Método para obtener los detalles de un plan de viaje, de la plataforma de plan viajes, devuelve la lista de gastos planeados.
* El web service soap recibe la respuesta del stored procedure y la devuelve por su response.

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP?wsdl` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP.WSMagicERPHttpSoap12Endpoint/` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A.
* **Recurso Postmam:** Obtener Detalles de Plan de Viaje (SOAP)

###### Procedimiento almacenado
* N/A - La lista de gastos se obtiene vía API del portal de plan de viajes
* **Parámetros:**

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:getPlanViajeDesgloseGastos"`

**Parámetros:**
* `compania`: Código de compañía
* `sucursal`: N/A
* `td`: N/A
* `nrodoc`: Número del plan de viaje requerido

**Request:**
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:getPlanViajeDesgloseGastos>
         <auth:compania>0033</auth:compania>
         <auth:sucursal></auth:sucursal>
         <auth:td></auth:td>
         <auth:nrodoc>49928</auth:nrodoc>
      </auth:getPlanViajeDesgloseGastos>
   </soap:Body>
</soap:Envelope>
```

**Response**
```bash
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getPlanViajeDesgloseGastosResponse xmlns:ns="http://auth.aje.com">
         <ns:return>
            <data>
               <web-service version="1.0"/>
               <erp id="Magic Software"/>
               <middleware api="jax-ws"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="51.0" importeTotalGasto="51.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="110.0" importeTotalGasto="110.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="95.0" importeTotalGasto="95.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="90.0" importeTotalGasto="90.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="148.0" importeTotalGasto="148.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="124.0" importeTotalGasto="124.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="174.0" importeTotalGasto="174.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="169.0" importeTotalGasto="169.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="233.0" importeTotalGasto="233.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="189.0" importeTotalGasto="189.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="220.0" importeTotalGasto="220.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="220.0" importeTotalGasto="220.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
               <pv-gasto aplicaTotal="No" compania="0033" descripcion="Alimentacion Nacional" diasPlanGasto="1" formaCalculo="Rango" gasto="12" importeGasto="220.0" importeTotalGasto="220.00" kilometros="" limiteMaximoGasto="550" nrodoc="49928" personas="1" rendimiento="" sucursal="" tarifaCombustible="" td="PVJ" tipoPV="N"/>
            </data>
         </ns:return>
      </ns:getPlanViajeDesgloseGastosResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### 4. Obtener Documentos (SOAP)

##### 1. Descripción
* Método para obtener la lista de documentos ordenes de giro pendientes de rendir, tipo Liquidación y Provisional.
* El web service soap recibe la respuesta del stored procedure y la devuelve por su response.

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP?wsdl` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP.WSMagicERPHttpSoap12Endpoint/` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A.
* **Recurso Postman:** Obtener Documentos (SOAP)

###### Procedimiento almacenado
* `USP_MAGICERP_GET_DOCS_ORIGEN_MX @P_COMPANIA CHAR(4), @P_PROVEEDOR_RFC CHAR(20)`
* **Parámetros:**
    * `@P_COMPANIA CHAR(4)` – Código de compañía del empleado
    * `@P_PROVEEDOR_RFC CHAR(20)` – Código de magic de empleado

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:getDocumentosOrigen"`

**Parámetros:**
* `compania`: Código de compañía del empleado
* `rfc`: Código de magic de empleado

**Request:**
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:getDocumentosOrigen>
         <!--Optional:-->
         <auth:compania>0060</auth:compania>
         <!--Optional:-->
         <auth:RFC>246228</auth:RFC>
      </auth:getDocumentosOrigen>
   </soap:Body>
</soap:Envelope>
```
##### response
```< Envelope soapenv="http://www.w3.org/2003/05/soap-envelope">
< Header/>
< Body>
< getDocumentosOrigenResponse ns="http://auth.aje.com">
< return>
<data>
<web-service version="1.0"/>
<erp id="Magic Software"/>
<middleware api="jax-ws"/>
<document ciaoco="" compania="0060" dococo="44716 " f_emision="2025-03-28 00:00:00.0" f_servicio=""
impoco="0" notas="Notas: Fecha Inicio: 2025-03-21, Fecha Fin: 2025-03-26, Fecha Solicitud: 2025-03-28, Tipo OG: liquidacion, No
PV: 44716, Autorizador: GUSTAVO MONTIEL GUZMAN" nrodoc=" 175913" pago="860.04" proveedor="" rfc="" sdoeva="0" sucoco=""
sucursal="01 " td="OGJ" tipoPV="N" tipodoc="L" trtoco=""/>

<document ciaoco="" compania="0060" dococo="44276 " f_emision="2025-03-05 00:00:00.0" f_servicio=""
impoco="0" notas="Notas: Fecha Inicio: 2025-02-01, Fecha Fin: 2025-02-28, Fecha Solicitud: 2025-03-05, Tipo OG: liquidacion, No
PV: 44276, Autorizador: GUSTAVO MONTIEL GUZMAN" nrodoc=" 175518" pago="2418.12" proveedor="" rfc="" sdoeva="0" sucoco=""
sucursal="01 " td="OGJ" tipoPV="N" tipodoc="L" trtoco=""/>

</data>
</ return>
</ getDocumentosOrigenResponse>
</ Body>
</ Envelope>
```

#### 5. Obtener Lista de Gastos (SOAP)

##### 1. Descripción
* Método para obtener la lista de de gastos disponibles para las rendiciones, la lista se obtiene del consolidado de magic y el portal de plan de viajes.

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP?wsdl` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP.WSMagicERPHttpSoap12Endpoint/` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A.
* **Recurso Postmam:** Obtener Lista de Gastos (SOAP)

###### Procedimiento almacenado
* 'N/A'

###### Consulta SQL
* `SELECT * FROM PV_TMP_GASTOSEXTRA WHERE ESTATUS = 'A' AND COMPANIA = :compania`
* **Parámetros:**
    * `@P_COMPANIA CHAR(4)` – Código de compañía para obtener la lista de gastos

###### Consulta SQL
* `SELECT * FROM PV_TMP_GASTOSFILTER WHERE PROCESAR = 'S' AND COMPANIA = :compania`
* **Parámetros:**
    * `@P_COMPANIA CHAR(4)` – Código de compañía para obtener la lista de gastos

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:getGastos"`

**Parámetros:**
* `compania`: Código de compañía

**Request:**
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:getGastos>
         <!--Optional:-->
         <auth:compania>0030</auth:compania>
      </auth:getGastos>
   </soap:Body>
</soap:Envelope>
```
##### response
```bash
<Envelope soapenv="http://www.w3.org/2003/05/soap-envelope">
    <Header/>
    <Body>
        <getGastosResponse ns="http://auth.aje.com">
            <return>
                <data>

                    <web-service version="1.0"/>
                    <erp id="Magic Software"/>
                    <middleware api="jax-ws"/>

                    <gasto compania="0030" descripcion="ALIMENTACION INTERNACIONAL"
                           fechaConsumo="SI" gasto="13" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="ALIMENTACION NACIONAL"
                           fechaConsumo="SI" gasto="12" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="ALQUILER SALA DE CONFERENCIAS"
                           fechaConsumo="SI" gasto="2020285" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="ANFITRIONAS Y MODELOS"
                           fechaConsumo="SI" gasto="2019378" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="ARTICULOS PROMOCIONALES"
                           fechaConsumo="SI" gasto="19403" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="AUTOBUS NACIONAL"
                           fechaConsumo="SI" gasto="16" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="BOLETO AVION INTERNACIONAL"
                           fechaConsumo="SI" gasto="33" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="BOLETO AVION NACIONAL"
                           fechaConsumo="SI" gasto="32" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="CASETA NACIONAL"
                           fechaConsumo="SI" gasto="14" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="CASETA INTERNACIONAL"
                           fechaConsumo="SI" gasto="24" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="CORREOS"
                           fechaConsumo="SI" gasto="2020473" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="DEPOSITO BANAMEX"
                           fechaConsumo="SI" gasto="99539" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="DEPOSITO BANCOMER"
                           fechaConsumo="SI" gasto="9931" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="DEPOSITO HSBC"
                           fechaConsumo="SI" gasto="99447" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="DEPOSITO SANTANDER"
                           fechaConsumo="SI" gasto="99244" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="ESTACIONAMIENTO INTERNACIONAL"
                           fechaConsumo="SI" gasto="25" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="ESTACIONAMIENTO NACIONAL"
                           fechaConsumo="SI" gasto="20" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="GASOLINA 87 OCTANOS MAGNA"
                           fechaConsumo="SI" gasto="17" importeCero="NO" kms="SI"/>

                    <gasto compania="0030" descripcion="GASOLINA 92 OCTANOS PREMIUM"
                           fechaConsumo="SI" gasto="19" importeCero="NO" kms="SI"/>

                    <gasto compania="0030" descripcion="GASTOS MEDICOS, MEDICINAS"
                           fechaConsumo="SI" gasto="2020472" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="HOSPEDAJE INTERNACIONAL"
                           fechaConsumo="SI" gasto="4" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="HOSPEDAJE NACIONAL"
                           fechaConsumo="SI" gasto="1" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="LAVANDERIA NACIONAL"
                           fechaConsumo="SI" gasto="23" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="MANTENIMIENTO AUTO"
                           fechaConsumo="SI" gasto="41" importeCero="NO" kms="NO"/>

                    <gasto compania="0030"
                           descripcion="MANTENIMIENTO Y REPARACION DE EQUIPO MOVIL"
                           fechaConsumo="SI" gasto="202048" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="PAPELERIA NACIONAL"
                           fechaConsumo="SI" gasto="27" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="PROMOTORES, DESGUSTADORAS"
                           fechaConsumo="SI" gasto="2020377" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="PROPINA"
                           fechaConsumo="SI" gasto="2019917" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="PRUEBA PCR COVID 19"
                           fechaConsumo="SI" gasto="40" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="RENTA AUTOMOVIL INTERNACIONAL"
                           fechaConsumo="SI" gasto="22" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="RENTA AUTOMOVIL NACIONAL"
                           fechaConsumo="SI" gasto="21" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="SERVICIOS DE DEGUSTACION"
                           fechaConsumo="SI" gasto="31" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="TAXI INTERNACIONAL"
                           fechaConsumo="SI" gasto="10" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="TAXI NACIONAL"
                           fechaConsumo="SI" gasto="7" importeCero="NO" kms="NO"/>

                    <gasto compania="0030" descripcion="VOUCHER GASOLINA"
                           fechaConsumo="SI" gasto="98539" importeCero="NO" kms="NO"/>

                </data>
            </return>
        </getGastosResponse>
    </Body>
</Envelope>
```


#### 6. Obtener sucursales (SOAP)

##### 1. Descripción
* Método para obtener la lista de sucursales de una compañía de magic.
* El web service soap recibe la respuesta del stored procedure y la devuelve por su response.

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP?wsdl` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP.WSMagicERPHttpSoap12Endpoint/` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A.
* **Recurso Postman:** Obtener sucursales (SOAP)

###### Procedimiento almacenado
* `USP_MAGICERP_SQL_SUCURSALES_MX @P_COMPANIA CHAR(4)`
* **Parámetros:**
    * `@P_COMPANIA CHAR(4)` – Código de compañía

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:getSucursales"`

**Parámetros:**
* `compania`: Código de compañía

**Request:**
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:getSucursales>
         <!--Optional:-->
         <auth:compania>0030</auth:compania>
      </auth:getSucursales>
   </soap:Body>
</soap:Envelope>
```
##### response
```bash
<Envelope soapenv="http://www.w3.org/2003/05/soap-envelope">
    <Header/>
    <Body>
        <getSucursalesResponse ns="http://auth.aje.com">
            <return>
                <data>

                    <web-service version="1.0"/>
                    <erp id="Magic Software"/>
                    <middleware api="jax-ws"/>

                    <sucursal compania="0030"
                               direccion="CALLE MANZANA A LOTE 7 PARQUE INDUSTRIAL SAN MIGUEL HUEJOTZINGO PUEBLA"
                               nombre="PLANTA PUEBLA"
                               sucursal="0001"/>

                    <sucursal compania="0030"
                               direccion="JAPETOS EDIFICIO 1 Y 2 PARCELA 3 No. 800 A 807 PARQUE INDUSTRIAL KALOS, GUADALUP"
                               nombre="PLANTA MONTERREY MAQUILA"
                               sucursal="0068"/>

                    <sucursal compania="0030"
                               direccion="CALLE 5 PARQUE INDUSTRIAL DEIT 103 ZI VILLAHERMOSA CENTRO TABASCO CP. 86280"
                               nombre="PLANTA VILLAHERMOSA MAQUILA"
                               sucursal="0070"/>

                    <sucursal compania="0030"
                               direccion="CARRETERA PANAMERICANA KM 1588 COL OBRERA MEOQUI CHIHUAHUA CP. 33130"
                               nombre="MAQUILA REFRESCOS UNION"
                               sucursal="0108"/>

                    <sucursal compania="0030"
                               direccion="MANZANA A LOTE 7 PQI SAN MIGUEL HUEJOTZINGO PUEBLA CP. 74160"
                               nombre="BASE DE BEBIDA EXPORTACION"
                               sucursal="0110"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA JOSE LOPEZ PORTILLO 299 COL EL ARBOL ECATEPEC DE MORELOS MEXICO CP."
                               nombre="PLANTA COACALCO"
                               sucursal="0111"/>

                    <sucursal compania="0030"
                               direccion="CALLE MANZANA A LOTE 8-12, PARQUE INDUSTRIAL SAN MIGUEL, HUEJOTZINGO, PUEBLA"
                               nombre="PUEBLA 1"
                               sucursal="02"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA VIA MORELOS s/n COL SAN JOSE JAJALPA ECATEPEC DE MORELOS MEXICO CP. 5"
                               nombre="ECATEPEC"
                               sucursal="08"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA DE LOS PARQUES 4 PQI PARQUE INDUSTRIAL KALOS SAN NICOLAS DE LOS GARZA"
                               nombre="SAN NICOLAS"
                               sucursal="100"/>

                    <sucursal compania="0030"
                               direccion="CALLE URANIO 401-6 COL 29 DE JULIO GUADALUPE NUEVO LEON CP. 67205"
                               nombre="EL MOLINETE"
                               sucursal="101"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA UNIVERSIDAD 13020 PQI INTERNACIONAL TIJUANA TIJUANA BAJA CALIFORNIA C"
                               nombre="TIJUANA"
                               sucursal="102"/>

                    <sucursal compania="0030"
                               direccion="CALLE URANIO 401 BODEGA 4 COL MISION DE SANTA CRUZ GUADALUPE NUEVO LEON CP. 6"
                               nombre="GUADALUPE 1"
                               sucursal="103"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA DEL TRABAJO 23 TEPOTZOTLAN MEXICO CP. 54605"
                               nombre="TEPOTZOTLAN"
                               sucursal="104"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA JOSÉ LÓPEZ PORTILLO 299 COL EL ARBOL ECATEPEC DE MORELOS MEXICO CP."
                               nombre="COACALCO"
                               sucursal="105"/>

                    <sucursal compania="0030"
                               direccion="CALLE 5 PARQUE INDUSTRIAL DEIT 103 ZI VILLAHERMOSA CENTRO TABASCO CP. 86280"
                               nombre="VILLAHERMOSA 1"
                               sucursal="106"/>

                    <sucursal compania="0030"
                               direccion="CALLE PASEO JAMAPA OTE 1803 URB VERACRUZ VERACRUZ VERACRUZ CP. 91966"
                               nombre="VERACRUZ"
                               sucursal="107"/>

                    <sucursal compania="0030"
                               direccion="AVENIDA HEROE DE NACOZARI 265 COL SECTOR LAS FLORES CAMPECHE CAMPECHE CP. 24"
                               nombre="CAMPECHE 2"
                               sucursal="108"/>

                    <sucursal compania="0030"
                               direccion="BLVRD VICENTE VALTIERRA 7020, FRACCIONES DE ALFARO, 37238 LEON, GTO"
                               nombre="LEON 1"
                               sucursal="109"/>

                    <sucursal compania="0030"
                               direccion="MEXIQUENSE 75, COACALCO, COACALCO DE BERRIOZÁBAL, MEX."
                               nombre="TULTITLAN 2"
                               sucursal="112"/>

                    <sucursal compania="0030"
                               direccion="GRAN CANAL 568, EL CHARCO ECATEPEC DE MORELOS, MEX, CP 55115"
                               nombre="ECATEPEC 2"
                               sucursal="113"/>

                    <sucursal compania="0030"
                               direccion="CIRCUITO, CAM. PARQUE INDUSTRIAL 278"
                               nombre="CENTRO DE CONSOLIDACION PUEBLA"
                               sucursal="115"/>

                    <sucursal compania="0030"
                               direccion="AV. FRANCISCO SARABIA N.1855 COL TERAN RUMBO A LA BASE AEREA MILITAR C.P. 29050"
                               nombre="TUXTLA GUTIERREZ"
                               sucursal="18"/>

                    <sucursal compania="0030"
                               direccion="CALLE OXIGENO 28 COL CIUDAD INDUSTRIAL CENTRO TABASCO CP. 86010"
                               nombre="VILLAHERMOSA"
                               sucursal="19"/>

                    <sucursal compania="0030"
                               direccion="CALLE CALLE 23 365 COL PASEOS DE ITZINCAB UMAN YUCATAN CP. 97390"
                               nombre="MERIDA"
                               sucursal="21"/>

                    <sucursal compania="0030"
                               direccion="LIBRAMIENTO LOPEZ PORTILLO 222-224 S/N COL ARTEAGA ARTEAGA COAHUILA CP. 25350"
                               nombre="SALTILLO"
                               sucursal="46"/>

                    <sucursal compania="0030"
                               direccion="MANZANA A LOTE DEL 8 AL 12 CORREDOR INDUSTRIAL QUETZALCOATL HUEJOTZINGO PUE"
                               nombre="CEDIS AUTOSERVICIOS PLANTA PUEBLA"
                               sucursal="56"/>

                    <sucursal compania="0030"
                               direccion="CARRETERA FEDERAL MEXICO PUEBLA KM 22.10 S/N ACAQUILPAN MEXICO CP. 5640"
                               nombre="LOS REYES LA PAZ"
                               sucursal="84"/>

                    <sucursal compania="0030"
                               direccion="CALLE PROFESOR AGUIRRE LAREDO 6715 COL PARTIDO LAS FUENTES CIUDAD JUAREZ CHIH"
                               nombre="CIUDAD JUAREZ"
                               sucursal="86"/>

                    <sucursal compania="0030"
                               direccion="CALLE 8 2566 ZI JALISCO GUADALAJARA JALISCO CP. 44940"
                               nombre="GUADALAJARA"
                               sucursal="95"/>

                </data>
            </return>
        </getSucursalesResponse>
    </Body>
</Envelope>
```
#### 7. Verificar email (SOAP)

##### 1. Descripción
* Método para validar mediante el email que un empleado esta vigente en la plataforma de plan de viajes.
* El web service soap recibe la respuesta del stored procedure y la devuelve por su response.

##### 2. Parámetros de Conexión
* **WSDL (DEV):** `http://10.0.56` (Solo accesible por VPN).
* **Endpoint (DEV):** `http://10.0.56.4:8181/aje-recepcion-cfdi-ws-bm/services/WSMagicERP.WSMagicERPHttpSoap12Endpoint/` (Solo accesible por VPN).
* **Método HTTP:** POST
* **Autenticación:** N/A.
* **Recurso Postmam:** Verificar email (SOAP)

###### Procedimiento almacenado
* `USP_MAGICERP_SQL_EMPLEADOS_EMAIL_MX @P_COMPANIA CHAR(4), @P_EMAIL VARCHAR(255)`
* **Parámetros:**
    * `@P_COMPANIA CHAR(4)` - Código de compañía del empleado
    * `@P_EMAIL VARCHAR(255)` - Correo electrónico del empleado

##### 3. Request
**Headers Requeridos:**
* `Content-Type: application/soap+xml; charset=utf-8`
* `SOAPAction: "urn:emailExistente"`

**Parámetros:**
* `compania`: Código de compañía del empleado
* `email`: Correo electrónico del empleado

**Request:**
```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:emailExistente>
         <!--Optional:-->
         <auth:compania>0033</auth:compania>
         <!--Optional:-->
         <auth:email>miguel.solis.mx@ajegroup.com</auth:email>
      </auth:emailExistente>
   </soap:Body>
</soap:Envelope>
```
##### response
```
< Envelope soapenv="http://www.w3.org/2003/05/soap-envelope">
< Header/>
< Body>
< emailExistenteResponse ns="http://auth.aje.com">
< return>
<data>
<web-service version="1.0"/>
<erp id="Magic Software"/>
<middleware api="jax-ws"/>
<empleado email_existente="1"/>
</data>
</ return>
</ emailExistenteResponse>
</ Body>
</ Envelope>
```

#### 8. Procedimientos para el registro de rendiciones en la MXBDAJE

##### 1. Descripción
* Se tiene un job en una aplicación web la cual ejecuta los siguientes stored procedures, para el registro de las rendiciones de gastos en la MXBDAJE

###### Procedimientos almacenados
* `USP_RFE_GEN_REND_GASTOS_LIQ @P_FECHACUSTOM CHAR(10)`
* `USP_RFE_GEN_REND_GASTOS_PROV @P_FECHACUSTOM CHAR(10)`
* **Parámetros:**
    * `@P_FECHACUSTOM` - Parámetro para especificar en que fecha se realizará el registro de las rendiciones

