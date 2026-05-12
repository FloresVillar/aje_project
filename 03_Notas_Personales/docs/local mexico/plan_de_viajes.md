## acceso a plan de viajes en test.docx 
Datos del usuario para el ambiente de test.
Portal de solicitudes / Plan viajes

https://testsolicitudes.ajemex.net/
Usuario: miguel.perez.mx
Pass: Qwerty123


## Actual Plan  Viajes-Flujo general.drawio.png

revisar [ARQUITECTURA_PLAN_VIAJES.md](../ARQUITECTURA_PLAN_VIAJES.md)

 

## Endpoints Plan viajes (SOAP) - 1.pdf

### Endpoints Plan viajes

Estos endpoint se generaron para sincronizar la información en el portal de plan de viajes.

> **Nota:**
> * No se proporcionan los ejemplos para su ejecución, debido a que sincronizan la información en el portal de plan de viajes y devuelven la respuesta del portal de plan de viajes, lo principal con estos métodos son los stored procedure que obtiene la información de magic.
> * Para realizar las pruebas se deben ejecutar los stored procedure que se indica en cada enpoint.

### Flujo sincronización de información al portal de plan de viajes

Cada punto consiste en invocar un api diferente:

1. ETL consulta datos empleados en bd DELSP.
2. ETL Consulta datos empleados en la bd MXBDAJE.
3. ETL Consulta datos de empleados del active directory.
4. ETL concentra información en bd DMRRHHMX.
5. Personal de TH completan información de los empleados y se guardan los cambios en le DMRRHHMX.
6. App en apache tomcat, ejecuta periódicamente la sincronización de empleados, áreas, compañías, etc al portal de plan de viajes.
    * Creación de nuevas compañías - `http://10.0.56`
    * Actualización de compañías - `http://10.0.56`
    * Sincronización de niveles - `http://10.0.56`
    * Creación de nuevas áreas - `http://10.0.56`
    * Actualización de áreas - `http://10.0.56`
    * Creación de nuevas ciudades - `http://10.0.56`
    * Actualización de ciudades - `http://10.0.56`
    * Creación de nuevos empleados - `http://10.0.56`
    * Validación de procesos de nomina - `http://10.0.56`
    * Actualización de empleados - `http://10.0.56`
7. Desde la MXBDAJE se consulta la DMRRHHMX para obtener los datos, los cuales son devueltos a la app de apache tomcat.
8. App apache tomcat envía los datos al portal de plan de viajes.
9. Portal de solicitudes valida permisos y envía los datos de nuevas ordenes de giro a la MXBDAJE. Revisar 
revisar [ARQUITECTURA_PLAN_VIAJES.md](../ARQUITECTURA_PLAN_VIAJES.md)

#### Parámetros de Conexión

* **Server (DEV):** `http://10.0.56.4:8181`
* **Método HTTP:** POST
* **Autenticación:** N/A.

#### Actualizar/Insertar empleados (SOAP)

##### 1. Descripción
* Método que obtiene los empleados de magic para enviarlos al portal de plan de viajes y sean actualizados o registrados en la plataforma.

##### 2. WSDL
* `http://10.0.56` - **Actualizar**
* `http://10.0.56` - **Insertar**

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE:
* `USP_PLANVIAJE_SQL_EMPLEADOS @P_COMPANIA CHAR(4), @P_TIPO CHAR(1)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar
* **@P_TIPO CHAR(1)** - Tipo de operación
    * **A** - Cuando se invoca el web service de Actualizar se envía el valor "**A**" para actualizar.
    * **I** - Cuando se invoca el web service de Insertar se envía el valor "**I**" para insertar nuevos registros.

Request SOAP

* El parámetro de compania pasa directo al stored procedure

```xml
<soap:Envelope xmlns:soap="http://w3.org" xmlns:ns="http://aje.com">
   <soap:Header/>
   <soap:Body>
      <ns:getData>
         <!--Optional:-->
         <ns:compania>0030</ns:compania>
      </ns:getData>
   </soap:Body>
</soap:Envelope>
```
 
Response SOAP

* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### Actualizar/Insertar áreas (SOAP)

##### 1. Descripción
* Método que obtiene las áreas de la bd DMRRHHMX para enviarlos al portal de plan de viajes y sean actualizados o registrados en la plataforma.

##### 2. WSDL
* `http://10.0.56` - **Actualizar**
* `http://10.0.56` - **Insertar**

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `USP_PLANVIAJE_SQL_AREA @P_COMPANIA CHAR(4), @P_TIPO CHAR(1)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar
* **@P_TIPO CHAR(1)** - Tipo de operación
    * **A** - Cuando se invoca el web service de Actualizar se envía el valor "**A**" para actualizar
    * **I** - Cuando se invoca el web service de Insertar se envía el valor "**I**" para insertar nuevos registros

##### 4. Request SOAP
* El parámetro de compania pasa directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:ws="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <ws:getData>
         <!--Optional:-->
         <ws:compania>0036</ws:compania>
      </ws:getData>
   </soapenv:Body>
</soapenv:Envelope>
```

##### 5. Response SOAP
* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### Actualizar/Insertar compañías (SOAP)

##### 1. Descripción
* Método que obtiene las compañías de magic para enviarlos al portal de plan de viajes y sean actualizados o registrados en la plataforma.

##### 2. WSDL
* `http://10.0.56` - **Actualizar**
* `http://10.0.56` - **Insertar**

##### 3. Procedimiento almacenado
* `USP_PLANVIAJE_SQL_COMPANIA @P_COMPANIA CHAR(4), @P_TIPO CHAR(1)`
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE.

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar
* **@P_TIPO CHAR(1)** - Tipo de operación
    * **A** - Cuando se invoca el web service de Actualizar se envía el valor "**A**" para actualizar
    * **I** - Cuando se invoca el web service de Insertar se envía el valor "**I**" para insertar nuevos registros

##### 4. Request SOAP
* El parámetro de compania pasa directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:ws="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <ws:getData>
         <!--Optional:-->
         <ws:compania>0036</ws:compania>
      </ws:getData>
   </soapenv:Body>
</soapenv:Envelope>
```

##### 5. Response SOAP
* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### Actualizar/Insertar ciudades (SOAP)

##### 1. Descripción
* Método que obtiene las ciudades de magic para enviarlos al portal de plan de viajes y sean actualizados o registrados en la plataforma.

##### 2. WSDL
* `http://10.0.56` - **Actualizar**
* `http://10.0.56` - **Insertar**

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `USP_PLANVIAJE_SQL_CIUDAD @P_COMPANIA CHAR(4), @P_TIPO CHAR(1)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar
* **@P_TIPO CHAR(1)** - Tipo de operación
    * **A** - Cuando se invoca el web service de Actualizar se envía el valor "**A**" para actualizar
    * **I** - Cuando se invoca el web service de Insertar se envía el valor "**I**" para insertar nuevos registros

##### 4. Request SOAP
* El parámetro de compania pasa directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:ws="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <ws:getData>
         <!--Optional:-->
         <ws:compania>0036</ws:compania>
      </ws:getData>
   </soapenv:Body>
</soapenv:Envelope>
```

##### 5. Response SOAP
* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### Validar/Actualizar procesos de nomina (SOAP)

##### 1. Descripción
* Método que actualiza en la bd DMRRHHMX, los empleados para sincronizarlos al portal de plan de viajes, de acuerdo a su proceso de nomina.

##### 2. WSDL
* `http://10.0.56`

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `USP_PLANVIAJE_VALIDA_PROCESO_NOMINA @P_COMPANIA CHAR(4)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar

##### 4. Request SOAP
* El parámetro de compania pasa directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:ws="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <ws:getData>
         <!--Optional:-->
         <ws:compania>0036</ws:compania>
      </ws:getData>
   </soapenv:Body>
</soapenv:Envelope>
```

##### 5. Response SOAP
* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### Enviar niveles (SOAP)

##### 1. Descripción
* Método que envía los niveles de empleados al portal de plan de viajes

##### 2. WSDL
* `http://10.0.56`

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `USP_PLANVIAJE_SQL_NIVEL @P_COMPANIA CHAR(4)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar

##### 4. Request SOAP
* El parámetro de compania pasa directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:ws="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <ws:getData>
         <!--Optional:-->
         <ws:compania>0036</ws:compania>
      </ws:getData>
   </soapenv:Body>
</soapenv:Envelope>
```

##### 5. Response SOAP
* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```
#### Actualizar/Insertar procesos de nomina (SOAP)

##### 1. Descripción
* Método que obtiene los procesos de nomina para enviarlos al portal de plan de viajes y sean actualizados o registrados en la plataforma.

##### 2. WSDL
* `http://10.0.56` - **Actualizar**
* `http://10.0.56` - **Insertar**

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `USP_PLANVIAJE_SQL_PROCESO_NOMINA @P_COMPANIA CHAR(4), @P_TIPO CHAR(1)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía a sincronizar
* **@P_TIPO CHAR(1)** - Tipo de operación
    * **A** - Cuando se invoca el web service de Actualizar se envía el valor "**A**" para actualizar
    * **I** - Cuando se invoca el web service de Insertar se envía el valor "**I**" para insertar nuevos registros

##### 4. Request SOAP
* El parámetro de compania pasa directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:ws="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <ws:getData>
         <!--Optional:-->
         <ws:compania>0036</ws:compania>
      </ws:getData>
   </soapenv:Body>
</soapenv:Envelope>
```

##### 5. Response SOAP
* Se devuelve return con el numero de registros actualizados en el portal de plan de viajes

```xml
<soapenv:Envelope xmlns:soapenv="http://w3.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getDataResponse xmlns:ns="http://aje.com">
         <ns:return>inserts: 0</ns:return>
      </ns:getDataResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

## Endpoint Plan de viajes (SOAP) - 2 .pdf

### Endpoints Plan viajes

Estos endpoint se utilizan para generar las ordenes de giro y validar que un usuario tenga permisos de generar un plan de viaje.

#### Validar permiso para generar OG (SOAP)

##### 1. Descripción
* Método que valida si un usuario tiene ordenes de giro pendientes de rendir, si tiene pendientes no puede generar otra orden de giro.

##### 2. WSDL
* `https://10.0.56`

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `[USP_PLANVIAJE_SQL_VALIDA_OG] @P_COMPANIA CHAR(4), @P_PROV_PAGO varchar(20)`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía del empleado en donde realiza el plan de viaje
* **@P_PROV_PAGO VARCHAR(20)** - Numero que tiene el empleado en Magic

##### 4. Request SOAP
* El parámetro de compania y provedor_pago pasan directo al stored procedure

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org" xmlns:auth="http://aje.com">
   <soapenv:Header/>
   <soapenv:Body>
      <auth:ValidaOG>
         <!--Optional:-->
         <auth:compania>0033</auth:compania>
         <!--Optional:-->
         <auth:provedor_pago>8936</auth:provedor_pago>
      </auth:ValidaOG>
   </soapenv:Body>
</soapenv:Envelope>
```

 ##### 5. Response SOAP
* Se devuelve return 1 = el usuario puede generar una OG, 0 = no puede generar orden de giro

```xml
<soapenv:Envelope xmlns:soapenv="http://xmlsoap.org">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:ValidaOGResponse xmlns:ns="http://aje.com">
         <ns:return>1</ns:return>
      </ns:ValidaOGResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Registrar orden de giro en Magic (SOAP)

##### 1. Descripción
* Método para registrar en magic una orden de giro con los datos que se envían del portal de viáticos

##### 2. WSDL
* `https://10.0.56`

##### 3. Procedimiento almacenado
* El web service ejecuta el stored procedure para obtener los datos de la MXBDAJE
* `USP_PLANVIAJE_SQL_INSERTA_OG_BG`

**Parámetros:**
* **@P_COMPANIA CHAR(4)** - Compañía
* **@P_PLAN_ID varchar(20)** - Nro de plan de viaje
* **@P_OBJETIVO varchar(300)** - Objetivo del plan de viaje
* **@P_SOLICITANTE varchar(20)** - Nro empleado de magic del solicitante
* **@P_PREPARADO varchar(20)** - Nro empleado de magic de la persona que genero el plan de viaje
* **@P_IMPORTE_TOTAL varchar(50)** - Importe total del plan de viaje
* **@P_TIPO varchar(50)** - Tipo liquidación / provisional
* **@P_APROBADOR1 VARCHAR(20)** - Nro empleado de magic del usuario aprobador N1
* **@P_APROBADOR2 VARCHAR(20)** - Nro empleado de magic del usuario aprobador N2
* **@P_FECAPRBA1 VARCHAR(20)** - Fecha aprobación N1
* **@P_FECAPRBA2 VARCHAR(20)** - Fecha aprobación N2
* **@P_MONEDA VARCHAR(10)** - Moneda

**Log de ejecución:**
`INFO 22:02:39.144 [https-jsse-nio-8443-exec-8] com.aje.auth.InsertaOG(InsertaOG.java:90): EXEC USP_PLANVIAJE_SQL_INSERTA_OG_BG '0060','50696','combustible','247999','247999','2000.00','provisional','106300','105479','2026-03-10 15:02:20','2026-03-10 15:02:20','PES'`
`INFO 22:02:39.428 [https-jsse-nio-8443-exec-8] com.aje.auth.InsertaOG(InsertaOG.java:102): USP_PLANVIAJE_SQL_INSERTA_OG_BG res: 181789`



```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:auth="http://auth.aje.com">
   <soap:Header/>
   <soap:Body>
      <auth:InsertaOGV2>
         <auth:compania>0060</auth:compania>
         <auth:plan_viaje_id>50696</auth:plan_viaje_id>
         <auth:objetivo>Combustible</auth:objetivo>
         <auth:solicitante>247999</auth:solicitante>
         <auth:preparado>247999</auth:preparado>
         <auth:total_plan_viaje>2000.00</auth:total_plan_viaje>
         <auth:tipo>provisiona</auth:tipo>
         <auth:aprobador1>106300</auth:aprobador1>
         <auth:aprobador2>105479</auth:aprobador2>
         <auth:fec_aproba1>2026-03-10 15:02:20</auth:fec_aproba1>
         <auth:fec_aproba2>2026-03-10 15:02:20</auth:fec_aproba2>
         <auth:moneda>PES</auth:moneda>
      </auth:InsertaOGV2>
   </soap:Body>
</soap:Envelope>
```

---

 Response SOAP

* Se devuelve return el numero de orden de giro, que se genero el magic

```xml
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:InsertaOGV2Response xmlns:ns="http://auth.aje.com">
         <ns:return>181754</ns:return>
      </ns:InsertaOGV2Response>
   </soapenv:Body>
</soapenv:Envelope>
```
