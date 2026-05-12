# Documentación técnica integrador maestros.DOCX

## 1. Contenido del documento

### 2. CONSIDERACIONES PREVIAS (Pág. 3)
* **2.1. URLS** (Pág. 3)
* **2.2. Lista resumen de servicios proporcionados** (Pág. 3)

### 3. Uso de servicio registra base de datos (Pág. 4)
* **3.1. Descripción** (Pág. 4)
* **3.2. Cuerpo** (Pág. 4)
* **3.3. Respuesta** (Pág. 4)

### 4. Uso de servicio registra procedimiento almacenado (Pág. 6)
* **4.1. Descripción** (Pág. 6)
* **4.2. Cuerpo** (Pág. 6)
* **4.3. Respuesta** (Pág. 7)

### 5. Uso de servicio ejecutar función (Pág. 8)
* **5.1. Descripción** (Pág. 8)
* **5.2. Cuerpo** (Pág. 8)
* **5.3. Respuesta** (Pág. 9)

### 6. Demostración de uso (Pág. 10)


## 2. CONSIDERACIONES PREVIAS

### 2.1. URLS


| Ambiente | Url |
| :--- | :--- |
| Desarrollo | `http://10.101.8` |
| Producción | `http://10.101.8` |

### 2.2. Lista resumen de servicios proporcionados


| Nombre | Url | Método | Header Auth | Origen | Destino |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Registrar base de datos | `/registraDB` | POST | Bearer token | Big Magic | Big Magic |
| Registrar Procedimiento almacenado | `/registraSP` | POST | Bearer token | Big Magic | Big Magic |
| Ejecutar funcion | `/ejecutaFuncion` | POST | Bearer token | Big Magic | Big Magic |


## 3. Uso de servicio registra base de datos

### 3.1. Descripción
Para uso del servicio se deberá haber generado previamente el token ("idToken") en la sección "Generar Token".


| | |
| :--- | :--- |
| **Nombre del método:** | Registrar base de datos |
| **Path:** | `/registraDB` |
| **Método HTTP:** | POST |
| **Descripción del Método:** | |
| **Sistema que invocará el servicio** | ERP |
| **Disponibilidad del servicio** | 24x7 |

### 3.2. Cuerpo
En el cuerpo (Body) de la consulta deberá ser de tipo "raw - JSON (application/json)" y enviar las siguientes propiedades:

```json
{
  "idCompania": "SELL",
  "nombreBD": "BDITEST",
  "instanciaBD": "172.32.0.32",
  "usuarioBD": "test",
  "claveBD": "123",
  "tipoBD": "O",
  "nombreUsuario": "ECALDAS"
}
```

### 3.3. Respuesta
**Status:** `200 OK`

```json
{
    "estado": "EXITO",
    "respuesta": "Registro Exitoso"
}
```

## 4. Uso de servicio registra procedimiento almacenado

### 4.1. Descripción
Para uso del servicio se deberá haber generado previamente el token ("idToken") en la sección "Generar Token".


| | |
| :--- | :--- |
| **Nombre del método:** | Registra procedimiento almacenado |
| **Path:** | `/registraSP` |
| **Método HTTP:** | POST |
| **Descripción del Método:** | |
| **Sistema que invocará el servicio** | ERP |
| **Disponibilidad del servicio** | 24x7 |

### 4.2. Cuerpo
En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar las siguientes propiedades:

```json
{
  "nemónico": "SP_TEST",
  "procedimiento": "TEST",
  "nombreUsuario": "SP_USER"
}
```
### 4.3. Respuesta

Y como datos de respuesta se obtendrá:

**Status:** `200 OK`

```json
{
    "estado": "EXITO",
    "respuesta": "Registro Exitoso"
}
```


## 5. Uso de servicio ejecutar función

### 5.1. Descripción
Para uso del servicio se deberá haber generado previamente el token ("idToken") en la sección "Generar Token".


| | |
| :--- | :--- |
| **Nombre del método:** | Registra procedimiento almacenado |
| **Path:** | `/ejecutaFuncion` |
| **Método HTTP:** | POST |
| **Descripción del Método:** | |
| **Sistema que invocará el servicio** | ERP |
| **Disponibilidad del servicio** | 24x7 |

### 5.2. Cuerpo
En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar las siguientes propiedades:

```json
{
  "nemonico": "RegistrarEmpleado",
  "idCompania": "0094",
  "tipoBD": "O",
  "trama": "",
  "nombreUsuario": "test"
}
```
### 5.3. Respuesta

Y como datos de respuesta se obtendrá:

```json
{
    "estado": "EXITO",
    "respuesta": "Registro Exitoso"
}
```


## 6. Demostración de uso

**PROCESO INTERCOMPANY**
Permite que el comprador pueda visualizar las guías VTC y facturas de venta del vendedor para poder generar la factura de compra. Básicamente, lo que hace es mostrar las ordenes de compra + nota de ingreso vs las guías VTC y la factura de venta de la compañía Intercompany, ejemplo Ajemex (comprador) y Alpamayo (vendedor).

El stored implementando es el : **PR_ERP_FNZ_QRY_GN_ObtenerOrdenCompraInterface**

```sql
CREATE PROCEDURE [dbo].[PR_ERP_FNZ_QRY_GN_ObtenerOrdenCompraInterface]
@P_Compania char(4),
@P_Sucursal char(4),
@P_Emisor char(4),
@P_FechaIni int,
@P_FechaFin int,
@P_Usuario char(10)
AS

--declare @P_Compania char(4)='0009'
--declare @P_Sucursal char(4)=''
--declare @P_Emisor char(4)='02'
--declare @P_FechaIni int=dbo.fc_integerdate('01/03/2023')
--declare @P_FechaFin int=dbo.fc_integerdate('31/03/2023')
--declare @P_Usuario char(10)='MOJEDA'

--exec PR_ERP_FNZ_QRY_GN_ObtenerOrdenCompraInterface '0009','03','02',738552,738579
--select dbo.fc_integerdate('01/02/2023')
--select dbo.fc_integerdate('28/02/2023')

BEGIN TRANSACTION [Tran2];
BEGIN TRY

INSERT INTO AUDITSP (NOMBRE, USUARIO, SERVIDOR, FECHA)
VALUES (OBJECT_NAME(@@PROCID), SYSTEM_USER, HOST_NAME(), GETDATE())

declare @NOMSTORE varchar(40) = LEFT('PR_ERP_FNZ_QRY_GN_ObtenerOrdenCompraInterface', 40)
declare @Parametro varchar(500) = 'PR_ERP_FNZ_QRY_GN_ObtenerOrdenCompraInterface'+ space(1) +
    '|COMPANIA='+LTRIM(rtrim(@P_Compania))+
        '|SUCURSAL='+LTRIM(rtrim(isnull(@P_Sucursal,'')))+
        '|EMISOR='+LTRIM(rtrim(@P_Emisor))+
        '|FECHAINI='+LTRIM(CONVERT(VARCHAR,DBO.FC_FECHA(@P_FechaIni),103))+
        '|FECHAFIN='+LTRIM(CONVERT(VARCHAR,DBO.FC_FECHA(@P_FechaFin),103))+
        '|USUARIO='+LTRIM(rtrim(@P_Usuario))

insert into CORREOMSG (
 COMPANIA
,USUARIO
,CODMOTIVO
,CO_ERRO
,MENSAJE
,TIPOMSJ
,ENVIADO
,FECENVIO
,HORENVIO
,NOMSTORE
,PARAMETRO
,FECCREA
,HORCREA
,USUCREA
,FECULTMOD
,HORULTMOD
,USUULTMOD
,ADICIONAL)
select @P_Compania [COMPANIA]
,@P_Usuario [USUARIO]
,'OBTIENEPF' [CODMOTIVO]
,'OBTIENEPF' [CO_ERRO]
,'OBTIENEPF' [MENSAJE]
,'E'
,'E'
,DBO.FC_INTEGERDATE(GETDATE())
,DBO.FC_HORA(GETDATE())
,@NOMSTORE
,@Parametro PARAMETRO
,DBO.FC_INTEGERDATE(GETDATE()) FECCREA

,DBO.FC_HORA(GETDATE()) HORCREA
,@P_Usuario USUCREA
,DBO.FC_INTEGERDATE(GETDATE()) FECULTMOD
,DBO.FC_HORA(GETDATE()) HORULTMOD
,@P_Usuario USUULTMOD
,@Parametro ADICIONAL


/** 0. CREAR VARIABLES PARA EL SERVICIO INTEGRADOR **/
DECLARE @PARAMETROS VARCHAR(MAX) = '';


--DECLARE @URL VARCHAR(MAX) = 'http://172.36.0 debe indicar la url al servicio del integrador


/**--NUEVO SERVIDOR EN AWS--**/
DECLARE @URL VARCHAR(MAX) = ''
DECLARE @URLMCORP VARCHAR(200)=(SELECT ISNULL(URLMCORP,'') FROM MPARAM2F WITH(NOLOCK) WHERE COMPANIA=@P_COMPANIA)


--SELECT @URLMCORP


SELECT @URL=ISNULL(@URLMCORP,'')
IF @URL=''
BEGIN
 set @URL = 'http://10.101.60'
END
/**--FIN NUEVO SERVIDOR EN AWS--**/


DECLARE @RESPONSE NVARCHAR(MAX);
DECLARE @OBJECT INT;
DECLARE @STATUS VARCHAR(100) = '';
DECLARE @RESPONSE_TEXT NVARCHAR(MAX)
DECLARE @RESPONSE_TABLE TABLE (RESPONSETEXT NVARCHAR(MAX))


/** 1. VERIFICAR LA SUCURSAL SI VIENE VACIO COLOCAR NULL **/
if @P_Sucursal=''

Begin
  set @P_Sucursal=Null
End


/** 2. OBTENER LAS OC SEGUN EL RANGO DE FECHA Y COLOCAR EN TABLA **/
DECLARE @DATOS_OBTENER_ORDEN_COMPRA_VALIDAS TABLE
(
 CIAORDCOMP CHAR(4),
 SUCORDCOMP CHAR(4),
 TRANSOCOMP CHAR(3),
 DOCORDCOMP CHAR(10),
 CIAINGRESO CHAR(4),
 SUCINGRESO CHAR(4),
 TRANSING CHAR(3),
 NRONOTAING CHAR(10),
 CIAEXPED CHAR(4),
 SUCEXPED CHAR(4),
 TRANSEXPED CHAR(3),
 NROEXPED CHAR(10),
 FECINGRESO INT,
 DOCUCOMALM CHAR(3),
 NROCOMALM2 CHAR(16),
 TIPORDCOMP CHAR(1),
 ARTORDEN FLOAT,
 SECORDCOMP SMALLINT,
 FECENT INT,
 SECING SMALLINT,
 TIPODOCREF CHAR(3),
 CiaBon char(4),
 SucBon char(4),
 TipDocBon char(4),
 NumBon char(10),

 NROCOMALM char(10)
)


INSERT INTO @DATOS_OBTENER_ORDEN_COMPRA_VALIDAS
SELECT
 OC4.CIAORDCOMP AS CIAORDCOMP,        
  OC4.SUCORDCOMP AS SUCORDCOMP,        
  OC4.TRANSOCOMP AS TRANSOCOMP,        
  OC4.DOCORDCOMP AS DOCORDCOMP,  
  LTRIM(RTRIM(OC4.CIAINGRESO)) AS CIAINGRESO,        
  LTRIM(RTRIM(OC4.SUCINGRESO)) AS SUCINGRESO,        
  LTRIM(RTRIM(OC4.TRANSING)) AS TRANSING,        
  LTRIM(RTRIM(OC4.NRONOTAING)) AS NRONOTAING,        
  LTRIM(RTRIM(OC4.CIAEXPED)) AS CIAEXPED,        
  LTRIM(RTRIM(OC4.SUCEXPED)) AS SUCEXPED,        
  LTRIM(RTRIM(OC4.TRANSEXPED)) AS TRANSEXPED,        
  LTRIM(RTRIM(OC4.NROEXPED)) AS NROEXPED,        
  LTRIM(RTRIM(OC4.FECINGRESO)) AS FECINGRESO,        
  LTRIM(RTRIM(Grem.DOCUCOMALM)) AS DOCUCOMALM,        
  LTRIM(RTRIM(Grem.NROCOMALM2)) AS NROCOMALM2,      
  LTRIM(RTRIM(OC4.TIPORDCOMP)) AS TIPORDCOMP,        
  LTRIM(RTRIM(OC4.ARTORDEN)) AS ARTORDEN,        
  LTRIM(RTRIM(OC4.SECORDCOMP)) AS SECORDCOMP,        
  LTRIM(RTRIM(OC4.FECENT)) AS FECENT,        
  LTRIM(RTRIM(OC4.SECING)) AS SECING,        
  LTRIM(RTRIM(OC4.TIPODOCREF)) AS TIPODOCRE,  
  LTRIM(RTRIM(isnull(Bonificacion.Compania,'') )) AS CiaBon,  
  LTRIM(RTRIM(isnull(Bonificacion.Sucursal,'') )) AS SucBon,  
  LTRIM(RTRIM(isnull(Bonificacion.PROCCOMALM,'') )) AS TipDocBon,  
  LTRIM(RTRIM(isnull(Bonificacion.NROMOVALM,'') )) AS NumBon,  
  
  LTRIM(RTRIM(Grem.NROCOMALM)) as [NROCOMALM]  
  
  FROM TORDCO4F OC4 WITH(NOLOCK)        
  INNER JOIN MPADIS1F Confg WITH(NOLOCK) ON (Confg.COMPANIA = OC4.CIAORDCOMP)      
  INNER JOIN MAPROB3F Aprob WITH(NOLOCK)   
   ON Aprob.COMPANIA = OC4.CIAORDCOMP   
   AND Aprob.MODULO = 'COL'   
   AND Aprob.OPCION = 'LG040'   
   AND Aprob.TRANSACCIO= 'OCO'        
  INNER JOIN TCOALM1F GRem WITH(NOLOCK)   
   ON GRem.COMPANIA = OC4.CIAINGRESO   
   AND GRem.SUCURSAL = OC4.SUCINGRESO   
   AND GRem.NROMOVALM = OC4.NRONOTAING
 AND GRem.STSCOMALM <> Confg.EGANULADA        
  INNER JOIN MCOMAFIL PAfil WITH(NOLOCK) ON (PAfil.COMPVEND = OC4.CIAEXPED AND PAfil.COMPCOMPR = OC4.CIAORDCOMP)   
  Left JOIN TCOALM1F Bonificacion WITH(NOLOCK)   
   ON Bonificacion.COMPANIA = OC4.CIAINGRESO   
   AND Bonificacion.SUCURSAL = OC4.SUCINGRESO   
   AND Bonificacion.ALMACENORI = OC4.EMISOR  
   AND Bonificacion.CIAREFER2 = GRem.CIAREFER2  
   AND Bonificacion.SUCREFER2 = GRem.SUCREFER2  
   AND Bonificacion.DOCUCOMAL2 = GRem.DOCUCOMAL2  
   AND Bonificacion.NROCOMALM2 = GRem.NROCOMALM2   
   AND Bonificacion.PROCCOMALM = 'BON'   
   AND Bonificacion.STSCOMALM <> Confg.EGANULADA    
  WHERE       
  OC4.CIAORDCOMP = @P_Compania  
  and OC4.SUCORDCOMP = Isnull(@P_Sucursal,OC4.SUCORDCOMP)  
  and OC4.EMISOR = @P_Emisor  
  and OC4.FLGFACTURA = 0x46        
  AND OC4.FECINGRESO BETWEEN @P_FechaIni AND @P_FechaFin     
  AND Aprob.EMPLEAPRO <> 0     
  AND OC4.ARTORDEN=0  
  AND (OC4.CIAEXPED<>'' AND OC4.CIAEXPED<>OC4.CIAORDCOMP)  
   
      
  --SELECT * FROM @DATOS_OBTENER_ORDEN_COMPRA_VALIDAS ORDER BY NRONOTAING      
   
  /** 3. OBTENER LOS DISTINTOS CIAEXPED **/      
  DECLARE @TBL_CIAEXPED TABLE (CIAEXPED CHAR(4))      
      
  INSERT INTO @TBL_CIAEXPED(CIAEXPED)      
  SELECT DISTINCT CIAEXPED      
  FROM @DATOS_OBTENER_ORDEN_COMPRA_VALIDAS     
  
  --select * from @TBL_CIAEXPED  
       
  /** 4. ORDENAR LOS CIAEXPED PARA RECORRIDO **/      
  DECLARE @TBL_CIAEXPED_SEND TABLE      
  (      
  ID INT,      
  CIAEXPED CHAR(4),      
 ESTADO INT      
  )      
      
  INSERT INTO @TBL_CIAEXPED_SEND      
  (      
  ID,       
  CIAEXPED,      
  ESTADO      
  )      
  SELECT       
  ROW_NUMBER() OVER(ORDER BY CIAEXPED ASC),      
  CIAEXPED,      
  0      
  FROM @TBL_CIAEXPED   
   
  --select * from @TBL_CIAEXPED_SEND  
      
  DECLARE @Min INT =  (SELECT MIN(ID) FROM @TBL_CIAEXPED_SEND)      
  DECLARE @Max INT =  (SELECT MAX(ID) FROM @TBL_CIAEXPED_SEND)   
    
  
  /** Tabla Para mostrar documentos **/      
  DECLARE @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA_FINAL TABLE        
  (        
  CIAORDCOMP CHAR(4),        
  SUCORDCOMP CHAR(4),       
  TRANSOCOMP CHAR(3),        
  DOCORDCOMP CHAR(10),            
  TIPORDCOMP CHAR(1),        
  ARTORDEN FLOAT,        
  SECORDCOMP SMALLINT,        
  FECENT INT,        
  SECING SMALLINT,            
  CIAINGRESO CHAR(4),        
  SUCINGRESO CHAR(4),        
  TRANSING CHAR(3),        
  NRONOTAING CHAR(10),          
  FECINGRESO INT,          
  CIAEXPED CHAR(4),        
 SUCEXPED CHAR(4),        
  TRANSEXPED CHAR(3),        
  NROEXPED CHAR(10),          
  COMPANIA CHAR(4),        
  SUCURSAL CHAR(4),        
  EMISOR CHAR(4),        
  DOCUCOMALM CHAR(3),        
  DOCUCOMVTA CHAR(3),        
  SERCOMVTA CHAR(10),        
  NROPRICOVT CHAR(16),        
  FECCOMPVTA INT,        
  MONEDA CHAR(4),        
  TIMPCOMVT FLOAT,        
  CLIENTE INT,        
  NROCOMVTA FLOAT,        
  NROCOMALM2 CHAR(16),        
  IP CHAR(30),        
  BASEDATOS CHAR(50),        
  TIPODOCREF CHAR(3),        
  TRANAFIL CHAR(4),         
  PROVEEDOR INT,  
     
  CiaBon char(4),  
  SucBon char(4),  
  TipDocBon char(4),  
  NumBon char(10),  
  
  NOMCLIENTE CHAR(80),  
  NOMSUCURSAL CHAR(40),  
  
  NROCOMALM char(10)  
  )       
  
  
  DELETE @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA_FINAL  
  
   
  /** 5.RECORRER CIAEXPED **/      
  WHILE (@Min IS NOT NULL AND  @Min <= @Max)
BEGIN      
      
    /** 6. OBTENER EL CIAEXPED  **/      
    DECLARE @CIAEXPED_TEMP VARCHAR(4) = (SELECT CIAEXPED FROM @TBL_CIAEXPED_SEND WHERE ID = @Min)      
      
    /** 7. TRAER DATOS DE TABLA CON CIAEXPED Y CONVERTIR A XML **/      
    DECLARE @SP_OBTENER_ORDEN_COMPRA_VALIDAS XML      
         
    SET @SP_OBTENER_ORDEN_COMPRA_VALIDAS =       
    (SELECT       
    CIAORDCOMP AS CIAORDCOMP,        
    SUCORDCOMP AS SUCORDCOMP,        
    TRANSOCOMP AS TRANSOCOMP,        
    DOCORDCOMP AS DOCORDCOMP,      
    LTRIM(RTRIM(CIAINGRESO)) AS CIAINGRESO,        
    LTRIM(RTRIM(SUCINGRESO)) AS SUCINGRESO,        
    LTRIM(RTRIM(TRANSING)) AS TRANSING,        
    LTRIM(RTRIM(NRONOTAING)) AS NRONOTAING,        
    LTRIM(RTRIM(CIAEXPED)) AS CIAEXPED,        
    LTRIM(RTRIM(SUCEXPED)) AS SUCEXPED,        
    LTRIM(RTRIM(TRANSEXPED)) AS TRANSEXPED,        
    LTRIM(RTRIM(NROEXPED)) AS NROEXPED,        
    LTRIM(RTRIM(FECINGRESO)) AS FECINGRESO,        
    LTRIM(RTRIM(DOCUCOMALM)) AS DOCUCOMALM,        
    LTRIM(RTRIM(NROCOMALM2)) AS NROCOMALM2,      
    LTRIM(RTRIM(TIPORDCOMP)) AS TIPORDCOMP,        
    LTRIM(RTRIM(ARTORDEN)) AS ARTORDEN,        
    LTRIM(RTRIM(SECORDCOMP)) AS SECORDCOMP,        
    LTRIM(RTRIM(FECENT)) AS FECENT,        
    LTRIM(RTRIM(SECING)) AS SECING,        
    '' AS IP,      
    '' AS BASEDATOS,      
    LTRIM(RTRIM(TIPODOCREF)) AS TIPODOCREF      
    FROM @DATOS_OBTENER_ORDEN_COMPRA_VALIDAS      
    WHERE CIAEXPED = @CIAEXPED_TEMP      
    FOR XML PATH)      
         
    /** 8. CONVERTIR EL XML A VARCHAR PARA ENVIO **/      
    DECLARE @SP_OBTENER_ORDEN_COMPRAS_VALIDAS_VARCHAR VARCHAR(MAX)
   
    SET @SP_OBTENER_ORDEN_COMPRAS_VALIDAS_VARCHAR = CONVERT(VARCHAR(MAX), @SP_OBTENER_ORDEN_COMPRA_VALIDAS)      
      
    /** 9. OBTENER LAS ORDENES DE COMPRA MEDIANTE SERVICIO  **/      
    DECLARE @SP_OBTENER_VENTAS_ORDENES_COMPRA XML      
    SET @SP_OBTENER_VENTAS_ORDENES_COMPRA = '' --ADD 27092020    
    -- ============================================================================================================================      
    DELETE @RESPONSE_TABLE;      
      
    ----Esta es la estructura JSON que se enviara hacia el servicio integrador      
    SET  @PARAMETROS = '{'+      
    '"nombreUsuario":"' + @P_Usuario + '",'+ --Esta variable indica el nombre de usuario / LJACINTO      
    '"nemonico":"SigcomtObtieneOC",'+ --Esta variable indica el nemonico(Stored Procedure) / SigcomtObtieneOC       
    '"idCompania":"' + @CIAEXPED_TEMP +'",'+ --Esta variable indica el codigo de compañia / COLUMNA CIAEXPED      
    '"tipoBD":"P",'+ --Esta variable indica el ambiente a ejecutar (P = PROD, Q = QA, D = DEV) / AHORA Q    
    --'"tipoBD":"Q",'+ --Esta variable indica el ambiente a ejecutar (P = PROD, Q = QA, D = DEV) / AHORA Q    
    '"trama":"' + @SP_OBTENER_ORDEN_COMPRAS_VALIDAS_VARCHAR +'"}'; --Esta variable indica los datos en varchar que se enviaran al SP / SE ENVIA XML      
      
    print @PARAMETROS  
  
    EXEC sp_OACreate 'MSXML2.ServerXMLHttp', @OBJECT OUT;      
    EXEC sp_OAMethod @OBJECT, 'Open', NULL, 'POST', @URL, 'false'      
    EXEC sp_OAMethod @OBJECT, 'SetRequestHeader', NULL, 'Content-Type', 'application/json'      
    EXEC sp_OAMethod @OBJECT, 'send', NULL, @PARAMETROS      
    EXEC sp_OAGetProperty @OBJECT, 'status', @STATUS OUT      
      
    INSERT INTO @RESPONSE_TABLE       
    EXEC sp_OAGetProperty @OBJECT, 'responseText'       
    EXEC sp_OADestroy @OBJECT      
      
    --select * from @RESPONSE_TABLE  
    --select * from @RESPONSE_TABLE wltr  
    SET @RESPONSE_TEXT = (SELECT RESPONSETEXT FROM @RESPONSE_TABLE)      

SELECT @SP_OBTENER_VENTAS_ORDENES_COMPRA = REPLACE(REPLACE(STRINGVALUE,'\u003c','<'),'\u003e','>')      
    FROM DBO.FC_PARSE_JSON(@RESPONSE_TEXT)      
    WHERE NAME = 'respuesta'      
    --=====================================================================================================================================      
      
    --select @SP_OBTENER_VENTAS_ORDENES_COMPRA      
      
  
    /** 10. CONVERTIR XML DE OBTENIDO DE SERVICIO A TABLA  **/      
    DECLARE @DATOS_OBTENER_VENTAS_ORDENES_COMPRA TABLE        
    (        
    COMPANIA CHAR(4),        
    SUCURSAL CHAR(4),        
    EMISOR CHAR(4),        
    DOCUCOMVTA CHAR(3),        
    NROCOMVTA FLOAT,        
    NROCOMALM CHAR(10),        
    DOCUCOMALM CHAR(3),        
    SERCOMVTA CHAR(10),        
    NROPRICOVT CHAR(16),        
    FECCOMPVTA INT,        
    MONEDA CHAR(4),        
    TIMPCOMVT FLOAT,        
    CLIENTE INT,  
      
    CIAINGRESO CHAR(4),        
    SUCINGRESO CHAR(4),        
    TRANSING CHAR(3),        
    NRONOTAING CHAR(10),        
    CIAORDCOMP CHAR(4),        
    SUCORDCOMP CHAR(4),        
    TRANSOCOMP CHAR(3),        
    DOCORDCOMP CHAR(10),  
  
    NOMCLIENTE CHAR(80),  
    NOMSUCURSAL CHAR(40)  
    
    )   
  DELETE @DATOS_OBTENER_VENTAS_ORDENES_COMPRA --ADD 27092020    
       
    INSERT INTO @DATOS_OBTENER_VENTAS_ORDENES_COMPRA        
    SELECT        
    Tbl.Col.value('COMPANIA[1]', 'CHAR(4)'),        
    Tbl.Col.value('SUCURSAL[1]', 'CHAR(4)'),        
    Tbl.Col.value('EMISOR[1]', 'CHAR(4)'),      
    Tbl.Col.value('DOCUCOMVTA[1]', 'CHAR(3)'),      
    Tbl.Col.value('NROCOMVTA[1]', 'FLOAT'),      
    Tbl.Col.value('NROCOMALM[1]', 'CHAR(10)'),      
    Tbl.Col.value('DOCUCOMALM[1]', 'CHAR(3)'),      
    Tbl.Col.value('SERCOMVTA[1]', 'CHAR(10)'),      
    Tbl.Col.value('NROPRICOVT[1]', 'CHAR(16)'),      
    Tbl.Col.value('FECCOMPVTA[1]', 'INT'),      
    Tbl.Col.value('MONEDA[1]', 'CHAR(4)'),      
    Tbl.Col.value('TIMPCOMVT[1]', 'FLOAT'),      
    Tbl.Col.value('CLIENTE[1]', 'INT') ,   
    Tbl.Col.value('CIAINGRESO[1]', 'char(4)'),    
    Tbl.Col.value('SUCINGRESO[1]', 'char(4)') ,   
    Tbl.Col.value('TRANSING[1]', 'char(3)') ,   
    Tbl.Col.value('NRONOTAING[1]', 'char(10)') ,   
    Tbl.Col.value('CIAORDCOMP[1]', 'char(4)'),  
    Tbl.Col.value('SUCORDCOMP[1]', 'char(4)'),  
    Tbl.Col.value('TRANSOCOMP[1]', 'char(3)'),  
    Tbl.Col.value('DOCORDCOMP[1]', 'char(10)'),  
    Tbl.Col.value('NOMCLIENTE[1]', 'char(80)'),  
    Tbl.Col.value('NOMSUCURSAL[1]', 'char(40)')  
    FROM  @SP_OBTENER_VENTAS_ORDENES_COMPRA.nodes('//row') Tbl(Col)         
      
    --select * from @DATOS_OBTENER_VENTAS_ORDENES_COMPRA  
  
    
  
    /** 11.CRUZAR DATA INICIAL CON DATA OBTENIDA DE SERVICIO **/      
    DECLARE @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA TABLE        
    (        
    CIAORDCOMP CHAR(4),        
    SUCORDCOMP CHAR(4),   
 TRANSOCOMP CHAR(3),        
    DOCORDCOMP CHAR(10),            
    TIPORDCOMP CHAR(1),        
    ARTORDEN FLOAT,        
    SECORDCOMP SMALLINT,        
    FECENT INT,        
    SECING SMALLINT,            
    CIAINGRESO CHAR(4),        
    SUCINGRESO CHAR(4),        
    TRANSING CHAR(3),        
    NRONOTAING CHAR(10),          
    FECINGRESO INT,          
    CIAEXPED CHAR(4),        
    SUCEXPED CHAR(4),        
    TRANSEXPED CHAR(3),        
    NROEXPED CHAR(10),          
    COMPANIA CHAR(4),        
    SUCURSAL CHAR(4),        
    EMISOR CHAR(4),        
    DOCUCOMALM CHAR(3),        
    DOCUCOMVTA CHAR(3),        
    SERCOMVTA CHAR(10),        
    NROPRICOVT CHAR(16),        
    FECCOMPVTA INT,        
    MONEDA CHAR(4),        
    TIMPCOMVT FLOAT,        
    CLIENTE INT,        
    NROCOMVTA FLOAT,        
    NROCOMALM2 CHAR(16),        
    IP CHAR(30),        
    BASEDATOS CHAR(50),        
    TIPODOCREF CHAR(3),        
    TRANAFIL CHAR(4),         
    PROVEEDOR INT,  
     
    CiaBon char(4),  
    SucBon char(4),  
    TipDocBon char(4),  
    NumBon char(10),  
 NOMCLIENTE CHAR(80),  
    NOMSUCURSAL CHAR(40),  
  
    NROCOMALM char(10)  
    )       
       
    DELETE @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA -- ADD 27092020    
       
    INSERT INTO @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA      
    SELECT         
    OC.CIAORDCOMP AS CIAORDCOMP,        
    OC.SUCORDCOMP AS SUCORDCOMP,        
    OC.TRANSOCOMP AS TRANSOCOMP,        
    OC.DOCORDCOMP AS DOCORDCOMP,              
    LTRIM(RTRIM(OC.TIPORDCOMP)) AS TIPORDCOMP,        
    LTRIM(RTRIM(OC.ARTORDEN)) AS ARTORDEN,        
    LTRIM(RTRIM(OC.SECORDCOMP)) AS SECORDCOMP,        
    LTRIM(RTRIM(OC.FECENT)) AS FECENT,        
    LTRIM(RTRIM(OC.SECING)) AS SECING,            
    LTRIM(RTRIM(OC.CIAINGRESO)) AS CIAINGRESO,        
    LTRIM(RTRIM(OC.SUCINGRESO)) AS SUCINGRESO,        
    LTRIM(RTRIM(OC.TRANSING)) AS TRANSING,        
    LTRIM(RTRIM(OC.NRONOTAING)) AS NRONOTAING,          
    LTRIM(RTRIM(OC.FECINGRESO)) AS FECINGRESO,          
    LTRIM(RTRIM(OC.CIAEXPED)) AS CIAEXPED,        
    LTRIM(RTRIM(OC.SUCEXPED)) AS SUCEXPED,        
    LTRIM(RTRIM(OC.TRANSEXPED)) AS TRANSEXPED,        
    LTRIM(RTRIM(OC.NROEXPED)) AS NROEXPED,          
    LTRIM(RTRIM(Ven.COMPANIA)) AS COMPANIA,        
    LTRIM(RTRIM(Ven.SUCURSAL)) AS SUCURSAL,        
    LTRIM(RTRIM(Ven.EMISOR)) AS EMISOR,        
    LTRIM(RTRIM(Ven.DOCUCOMALM)) AS DOCUCOMALM,          
    LTRIM(RTRIM(Ven.DOCUCOMVTA)) AS DOCUCOMVTA,        
    LTRIM(RTRIM(Ven.SERCOMVTA)) AS SERCOMVTA,        
    LTRIM(RTRIM(Ven.NROPRICOVT)) AS NROPRICOVT,        
    LTRIM(RTRIM(Ven.FECCOMPVTA)) AS FECCOMPVTA,        
    LTRIM(RTRIM(Ven.MONEDA)) AS MONEDA,        
    Ven.TIMPCOMVT AS TIMPCOMVT,   -- CHANGE 13102020DTL   
 LTRIM(RTRIM(Ven.CLIENTE)) AS CLIENTE,        
    Ven.NROCOMVTA AS NROCOMVTA,        
    LTRIM(RTRIM(OC.NROCOMALM2)) AS NROCOMALM2,        
    '' AS IP,      
    '' AS BASEDATOS,      
    LTRIM(RTRIM(OC.TIPODOCREF)) AS TIPODOCREF,      
    LTRIM(RTRIM(Confg.TRANAFIL)) AS TRANAFIL,      
    PAfil.PROVEEDOR AS PROVEEDOR  ,  
     
    CiaBon,  
    SucBon,  
    TipDocBon,  
    NumBon,  
  
    NOMCLIENTE,  
    NOMSUCURSAL,  
  
    OC.NROCOMALM   
  
    FROM @DATOS_OBTENER_VENTAS_ORDENES_COMPRA Ven        
    INNER JOIN @DATOS_OBTENER_ORDEN_COMPRA_VALIDAS OC        
     on Ven.COMPANIA  = OC.CIAEXPED        
     AND Ven.SUCURSAL = OC.SUCEXPED        
     AND Ven.NROCOMALM = OC.NROEXPED        
     AND Ven.DOCUCOMALM = OC.TRANSEXPED    
     AND Ven.CIAORDCOMP = OC.CIAORDCOMP  
     AND Ven.SUCORDCOMP = OC.SUCORDCOMP  
     AND Ven.TRANSOCOMP = OC.TRANSOCOMP  
     AND LTRIM(RTRIM(Ven.DOCORDCOMP)) = LTRIM(RTRIM(OC.DOCORDCOMP))  
     AND Ven.CIAINGRESO = OC.CIAINGRESO  
     AND Ven.SUCINGRESO = OC.SUCINGRESO  
     AND Ven.TRANSING = OC.TRANSING  
     AND Ven.NRONOTAING = OC.NRONOTAING  
    INNER JOIN MTRANAFIL Confg WITH(NOLOCK)         
     On Confg.COMPANIA = Ven.COMPANIA        
     AND Confg.TRANSACCIO= Ven.DOCUCOMVTA        
     AND Confg.COMPAFIL = OC.CIAORDCOMP        
    INNER JOIN MCOMAFIL PAfil WITH(NOLOCK)        
     on PAfil.COMPVEND = OC.CIAEXPED    
AND PAfil.COMPCOMPR = OC.CIAORDCOMP        
    LEFT JOIN TFACOM1F FAC WITH(NOLOCK)   
     on FAC.COMPANIA  = OC.CIAORDCOMP        
     AND FAC.SUCURSAL = OC.SUCORDCOMP        
     AND FAC.TRANSACCIO = Confg.TRANAFIL        
     AND FAC.NROSERIE = VEN.SERCOMVTA        
     AND FAC.NRODOC  = VEN.NROPRICOVT        
     AND FAC.PROVEEDOR = PAfil.PROVEEDOR   
    LEFT JOIN TFACAFIL1F Interface WITH(NOLOCK)   
     on FAC.COMPANIA  = OC.CIAORDCOMP        
     AND FAC.SUCURSAL = OC.SUCORDCOMP        
     AND FAC.TRANSACCIO = Confg.TRANAFIL        
     AND FAC.NROSERIE = VEN.SERCOMVTA        
     AND FAC.NRODOC  = VEN.NROPRICOVT        
     AND FAC.PROVEEDOR = PAfil.PROVEEDOR   
    WHERE         
    FAC.COMPANIA IS NULL     
    and Interface.COMPANIA IS NULL  
    
    --select * from @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA  
  
    /*-- Guardar Informacion para mostrar en pantalla--*/  
    INSERT INTO @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA_FINAL  
    SELECT   
    CIAORDCOMP,        
    SUCORDCOMP,        
    TRANSOCOMP,        
    DOCORDCOMP,              
    TIPORDCOMP,        
    ARTORDEN,        
    SECORDCOMP,        
    FECENT,        
    SECING,            
    CIAINGRESO,        
    SUCINGRESO,        
    TRANSING,        
    NRONOTAING,          
    FECINGRESO,          
    CIAEXPED,
 SUCEXPED,        
    TRANSEXPED,        
    NROEXPED,          
    COMPANIA,        
    SUCURSAL,        
    EMISOR,        
    DOCUCOMALM,          
    DOCUCOMVTA,        
    SERCOMVTA,        
    NROPRICOVT,        
    FECCOMPVTA,        
    MONEDA,        
    TIMPCOMVT,   -- CHANGE 13102020DTL     
    CLIENTE,        
    NROCOMVTA,        
    NROCOMALM2,        
    [IP],      
    [BASEDATOS],      
    TIPODOCREF,      
    TRANAFIL,      
    PROVEEDOR  ,  
     
    CiaBon,  
    SucBon,  
    TipDocBon,  
    NumBon,  
  
    NOMCLIENTE,  
    NOMSUCURSAL,  
  
    NROCOMALM  
    FROM @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA  
      
      
  
    /** 23. ACTUALIZAMOS EL ESTADO DEL CIAEXPED **/      
    UPDATE @TBL_CIAEXPED_SEND SET ESTADO = 1 WHERE ID = @Min      
      
    /** 24.SELECCIONAR EL SIGUIENTE CIAEXPED **/      
SELECT @Min  = MIN(ID) FROM  @TBL_CIAEXPED_SEND WHERE ID >= @Min AND ESTADO = 0      
        
   END    
  
  SELECT   
  /*--Datos Orden de Compra--*/  
  Datos.CIAORDCOMP  
  ,Datos.SUCORDCOMP  
  ,Datos.TRANSOCOMP  
  ,Datos.DOCORDCOMP  
    
  /*--Datos Factura Venta--*/  
  ,Datos.COMPANIA  
  ,Datos.SUCURSAL  
  ,Datos.DOCUCOMVTA  
  ,Datos.SERCOMVTA  
  ,Datos.NROPRICOVT  
  ,Datos.CLIENTE  
  ,Datos.EMISOR  
  ,Datos.NROCOMVTA  
  
  /*--Datos Nota de Ingreso--*/            
  ,Datos.CIAINGRESO  
  ,Datos.SUCINGRESO  
  ,Datos.TRANSING  
  ,Datos.NRONOTAING  
      
  ,Datos.FECINGRESO  
  --,convert(varchar,dbo.fc_fecha(FECINGRESO),103) FECINGRESO  
      
  ,Datos.CIAEXPED  
  ,Datos.SUCEXPED  
  ,Datos.TIPODOCREF  
  ,Datos.NROCOMALM2  
  
  /*--Datos Bonificacion--*/  
  ,Datos.CiaBon  
  ,Datos.SucBon  
  ,Datos.TipDocBon  
,Datos.NumBon  
  ,Datos.NROEXPED     
      
  /*--Datos Adicionales--*/  
  ,Datos.FECENT  
  --,convert(varchar,dbo.fc_fecha(FECENT),103) FECENT  
      
  ,Datos.FECCOMPVTA  
  --,convert(varchar,dbo.fc_fecha(FECCOMPVTA),103) FECCOMPVTA  
  
  ,Datos.MONEDA  
  ,Datos.TIMPCOMVT  
  ,Datos.TRANAFIL  
  ,Datos.PROVEEDOR  
    
  ,Sucursal.NOMBRE [NombreSuc]  
  ,Origen.NOMBRE [NombreCiaOrig]  
  ,Almacen.DESCEMISOR [NombreEmisor]  
  ,Proveedor.NOMBRE [NombreProv]  
  
  ,Datos.NOMCLIENTE  
  ,Datos.NOMSUCURSAL  
  
  ,Datos.DOCUCOMALM  
  ,Datos.NROCOMALM  
  FROM  @DATOS_CRUZAR_ORDEN_COMPRA_FACTURA_VENTA_FINAL Datos  
  inner join Tcompa2f Sucursal with(nolock) on (Datos.CIAORDCOMP=Sucursal.COMPANIA and Datos.SUCORDCOMP=Sucursal.SUCURSAL)  
  inner join mcompa1f Origen with(nolock) on (Datos.COMPANIA=Origen.COMPANIA )  
  left join memiso1f Almacen with(nolock) on (Datos.CIAORDCOMP=Almacen.COMPANIA and Datos.SUCORDCOMP=Almacen.SUCURSAL and Datos.EMISOR=Almacen.EMISOR)  
  inner join mpersodf Proveedor with(nolock) on (Datos.CIAORDCOMP=Proveedor.COMPANIA and Datos.PROVEEDOR=Proveedor.PROVEEDOR  )  
  where Datos.CIAORDCOMP=@P_Compania  
    
  
  
 COMMIT TRANSACTION [Tran2]     
 END TRY      
 BEGIN CATCH      
PRINT ERROR_MESSAGE()      
  ROLLBACK TRANSACTION [Tran2]      
 END CATCH 

```