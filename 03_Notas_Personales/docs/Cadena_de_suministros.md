parafraseado de gemini
## Avail

### Boms.docx 
Este documento es util para ver como se estructuran las recetas de los productos terminandos en cadena de suministros de AJE.
Tecnicamente es la especificacion de la interfaz de datos para el modulo de la cadena de suministro(supply chain).Le dice al desarrollador(o sistema de integracion  ) que datos debe extraer del ERP y como deben enviarse.

Un Bill of Materials (BOMs) es la formula tecnica para un producto terminado.

El documento muestra dos secciones: **Properties** y **Require Attributes** 

#### Properties(Metadatos del proceso)
Es la parte de la identidad del paquete de datos que se va a mover.

- Parcel Type (BOMs) Indica que el contenido del envio son los bill of materials(las recetas de fabricacion).En el sistema , cada tipo de dato (cliente, inventario, receta) tiene un **Parcel Type** distinto para que el receptor sepa que procesar. 

- Interface Table Name(IBOMs) Es el nombre de la tabla temporal o "staging" donde se van a insertar los datos antes de ser validados. Es como un 'anden de carga' que va al almacen principal.

#### Required Attributes (El contrato de datos)
Define la informacion obligatoria para que la receta sea valida.Cada atributo tine el nombre, tipo de dato, descripcion  y ademas un ejemplo.Hay dos clases de atributos , aquellos que son IDs y los que son cantidades.
- Indentificadores(IDs):
    - **parcelld** : 
    - **BomMVerCd** : identificador unica de version del BOM **92001**
    - **MakeItemCd** : tal como lo indica la descripcion es el codigo del producto final **501068**
    - **UseItemCd** Es la materia prima (azucar, goma, etiqueta)
    - **BomNM** : nombre del BOM
 
- Cantidades
    - **UsePer** : Indica cuánto de ese material se ua para producir una unidad (caja) del producto final. **0.33005537**
    - **UsePerCO** : Es el uso durante el CHANGEOVER(el arranque de maquina). Es vital para calcular el costo real de produccion.
    - **WastePct** : porcentaje de perdida.

Como se integra dentro del proyecto ?

- Los datos fluyen desde ERP Big Magic(via terminal Service/RDP en el server SRVGLTS36) Dentro de este entorno , se ejecuta el Stored procedure **AV10_IBOMI**[conectividad] que empaqueta la receta (BOM) en un formato que se puede exportar.

- La transformacion , punto medio : ahora los datos viajan al servidor **RVGAPPCT58** , donde ocurre la limpieza .El ERP puede entregar los datos en formatos antiguos , este servidor SQL intermedio los normaliza para que quede como la tabla IBOMS visto antes.
- El motor de movimiento **AWS Glue** : El  job de AWS Glue **ETLIbomsJob-Corp**.[conectividad]() es el "camion" que se conecta al servidor intermedio **SRVGAPCT58** recoge los datos ya normalizados y los sube a la nube. Glue es una herramienta que puede conectar el mundo On-Premise (servidores locales) con la nube de AWS.
- El job Glue termina su recorrido depositando los datos en la base de datos de postgres(A10_SOUTH) en AWS que es el corazon de datos que utiliza el sistema AVAIL para que los plainificadores vean las recetas.
 
Resumen : El job de AWS Glue (**ETLIbomsHob-Corp**) hace la conexion → El Stored Procedure **AV10_IBOMI** ejecuta → pasando a los servidores **SRVGLT36** (RDP) y **SRVGAPPCT58**(SQL transformacion) → finalmente llega a la base de datos **A10_SOUTH** para que AVAIL lo use.


```bash
ESTRATOS FÍSICOS Y LÓGICOS DE INTEGRACIÓN (BOMs)
      ─────────────────────────────────────────────────

      [ ON-PREMISE / DATA CENTER ]             [ CLOUD (AWS) ]
      ────────────────────────────             ───────────────
      
   (1) ORIGEN: BIG MAGIC (ERP)
       Server: SRVGLTS36 (RDP)
       Soft: Store Procedure AV10_IBOMI
                │
                │ (Extracción de Recetas)
                ▼
   (2) INTERMEDIO: SQL SERVER 
       Server: SRVGAPCT58                      (3) MOTOR DE MOVIMIENTO
       Acción: Normalización de                 AWS GLUE (Serverless)
               Esquemas (Tabla IBOMS)           Job: ETLIbomsJob-Corp
                │                                      │
                │◀─────────────────────────────────────┘
                │ (Lectura vía Conector JDBC/Red)
                │
                ▼
   (4) DESTINO: POSTGRES RDS
       Database: A10_SOUTH
       Sistema: AVAIL (Supply Chain)
                │
                ▼
      [ Planificación de Producción ]
```
### conectividad y sincronizacion con AVAIL mmediante ETL.docx

Los datos se entregan desde ERP Big Magic hacia el sistema AVAIL mediante procesos ETL(extraccion , transformacion y carga). 

Se intenta garantizar la sincronizacion de inteligencia operativa y los recursos gestionados en Big Magic. 

#### Proposito de la integracion

- Sincronizacion transacccional: trasladar los registros maestros y otros
- integridad de las reglas de negocio: adaptar los datos de Big Magic a validaciones de AVAIL
- optimizacion de workflows: minimizar la latencia entre creacion de un registro ERP y disponibilidad.

#### componentes del flujo ETL 

- Extraccion (Big Magic): Metodos de consulta mediante Store Procedures a las bases de datos en Big Magic. Identificando deltas y cambios e inventarios en tiempo real para procesos en AVAIL.

- Transformacion : normalizacion de esquemas , conversion de tipos de datos y mapeo de logica propietaria de Big Magic a las estructuras compatibles con AVAIL.

- Carga(AVAIL): ingesta de datos mediante puntos de acceso autorizados, asegurando el cumplimiento de las restricciones de integridad de AVAIL.

Importancia estrategica: Esta conectividad es vital para la continuidad operativa, permitiendo que el equipo de trabajo cuente con informacion actualizada en AVAIL sin necesidad de relaizar capturas manuales de datos ya existentes en Big Magic.

Los parametros de conexion deben ser tratados como informacion sensible...

#### Configuracion de conexion en origin : Big magic (via terminal services)

El acceso a los datos de origen no es directo desde la red externa, la extraccion se realiza estableciendo uuna sesion de Terminal Services(RDP) para interactuar con el motor de base de datos seguro y segregado mediante el sever name **SRVGLTS36**

#### Configuracion de conexion intermedia : SQL transformacion (via terminal services)

En este caso se usa SRVGAPCT58 para establecer una conexion RDP a la base de datos

#### Configuracion de conexion en Destino: POSTGRES (via terminal services)

En este caso se usa **SRVGAPCT58**.

Dado que el origen Big MAgic requiere el acceso via RDP , el script python en Glue actuara como el orquestador que se conecta a los diferentes entornos para extraer los datos y llevarlos a AVAIL.

Se describen los jobs alojados en la Cuenta (cadena DEV ...) de AWS Glue diseñados para la extraccion desde Big Magic y carga en AVAIL. 

Es util revisar el documento original .

Siempre es mas grato que la ia sintice y humanice la teoria.

#### En la simulacion
##### El mapa de credenciales (seguridad y conectividad) 
Existen 3 nodos criticos por los que se enrutaran los datos.Se ha de configurar el contenedor **integrador_api** con variables de entorno:
- **origen(Big Magic)**: **SEVGLZADB01** en el puerto 54241
- Intermedia(SQL transformacion) : IP 10.100.199.0 puerto 1433, aqui vive la tabl IBOMS
- Destino(CLoud): Una instancia de RDS Postgres en AWS (**rds-postgresql-avail-latam.sur...**)

##### El catalogo de Jobs de AWS Glue

Ahora sabemos que no solo movemos recetas (BOMS). Las capturas muestran una suite completa de procesos ETL que podrian emular:
- **ETLtems-job-Corp**: Mueve articulos de producto terminado (PT) y Materia Prima (MP)
- **ETLInvAcstJob-Corp** Sincroniza inventarios
- **ETLMakeAcstJob-Corp** cumplimiento del plan de produccion.
- **ETLBomsJob-Corp** Recetas

##### La logica Bidireccional(AVAIL-BM) 
Un detalle crucial es que el flujo no es solo Big Magic hacia AVAIL , existen procesos de retorno.
- **ETLMakeSegmentJob-Corp** Envia el plan de produccion generado en AVAIL de vuelta a Big Magic
- **ETLShipSchdJob-Corp** Envia el plan de distribucion

##### Modificaciones de los scripts
1. En **as400_core** se crea la tabla (csv) **mpersoeff_bomc.csv** con las columnas exactas (**MakeeItemCd**,**BomVerCd**,**UsePer**)

2. En **integrador_api** Añadimos en un endpoint llamado **/aws_glue/sync_boms**. Cuando este sea invocado leera los datos del core, aplicara la logica de "transformacion" , ej : validando que **WastePct** sea un numero y lo sube a destino.
3. En **fabric_monitor** Ahora no solo mira la nomina , sin que compara lo que se produce en la receta **IBOMS** para detectar desviacions de costo.

### InvActs.docx 

Describe los detalles de Inventarios reales. Se simulará no solo qué deberia pasar(bomb) sino qué esta pasando fisicamente en el almacen de AJE.

Que datos viajan en el paquete **InvActs** , segun los estandares de AJE .
1. Identificadores de ubicacion y producto: 
    - LocCd (Location Code) es el codigo de la planta o centro de distribucion (ej 8502)
    - ItemCd ( Item Code) es el codigo unico del producto o materia prima, es el nexo que une esta tabla con la de Boms

2. Datos y cantidad y estado
    - InvQty (Invetory Quanty) la cantidad fisica contada, es un valor decimal (ej 8040-0000)
    - AvailQty ;(Available Quantity) no siempre es igual a la anterior, representa lo que esta libre para usar
    - HoldQty (Hold Quantity) mercancia que esta en el almacen pero "bloqueado" por control de calidad o dañada.

3. Atributos de tiempo y registro (criticos para ETL) 
    - AsOfStamp (As of Date/time): la marca de tiempo exacta de cuando se tomo lectura en el ERP.Evita que el sistema use datos obsoletos

    - InvTm(inventory time) hora especifica del registro , necesaria para la precision en el motor AVAIl.

4. Metadatos de integracion 
    - Parcel Type(INVACTS) la etiqueta que le dice  ASW Glue, este paquete es de inventarios , no son nominas ni recetas
    - Iterface Table Name (IINVACTS) el nombre de la tabla puente, donde caeran los datos antes de entrar al postgres final.

### Items.docx
**Un producto es una combinacion de tipo , variedad y opcionalmente variante**. El nombre corto del producto debe contener dos elementos ej : 15OZ_CN1/12_BSTDTSODA 

- tipo      :   15OZ_CN1/12
- variedad  :   BSTDTSODA

1. **Identidad y clasificacion**: Estos campos perrmiten que el sistema AVAIL agrupe los productos para reportes gerenciales 
    - **ItemCd & ItemNm** : el codigo alfanumerico (ej 13439) y el nombre largo descriptivo (150Z CN 1/12 DTSODA)
    - **KindCd & VarietyCd** : clasificacion tecnica . El kind define la naturaleza (ej Gaseosa) y Variety (el sabor o tipo especifico)
    - itemTag1 (familia): Etiqueta de agrupacion superior como **CSD(carbonated soft drinks)**
    - Variant : Atributo para distinguir versiones de un mismo producto, como una edicion de exportacion.
2. **Flags de estados** (las reglas del negocio): Estas son caracteres de un solo digito (Y/N) que le dicen al integrador como tratar el dato
    - IsProd (Is Produced) : indica si el item sale de un linea de produccio nde AJE 
    - IsMatl (is material) : Indica si es materi prima (aucar, preformas, etiquetas)
    - IsWIP (Work in progress) : para productos intermedios , como el jarabe (Syrup) que aun no ha sido embotellado.
    - IsPal ( Is Pallet) : Define si el item es una unidad de transporte (pallet)
    - IsBusy & IsSell : Determinan si el item se compra a proveedores o se vende directamente a cliente.
3. **Atributos fiscicos y logisticos** (La inteligencia de carga) Cruciales para que el fabric_monitor calcule pesos y volumenes de despacho.
    - **BaseUoM** (base unit of measure) la unidad minima de inventario , por ejemplo, CASE (caja) o BIB (bag-in-box)
    - **BaseWt** (Base Weight) el peso de la unidad (ej 6.37) es vital para no sobrecargar los camiones en la simulacion de despacho
    - **ShipWt** (Ship Weight) El peso total cuando se envia en unidades mayores, como un pallet completo (ej 1350)

### KINDS.docx
Definición de Kinds

Un **Kind**, o paquete de producto, es un atributo de un producto. El nombre corto del Kind debe contener tres elementos. Usando 15OZCN1/12 como ejemplo:

* **Size**– 15OZ
* **Container type** – CN
* **Packaging** – 1/12

#### Propiedades de la Interfaz (Properties)

* **Parcel Type**: KINDS
* **Interface Table Name**: IKINDS

#### Atributos Detallados (Required Attributes)

| Atributo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento load_parcel | |
| **KindCd** | Character(25) | Identificador alfanumérico único | 02 |
| **Kind** | Character(25) | Nombre corto único | 15OZ_CN1/12 |
| **KindNm** | Character(100) | Nombre largo | 15OZ CN 1/12 |
| **KindTag1** | Character(64) | Contenedor | CAN |
| **KindSeq** | Character(25) | Secuencia de Kinds en editores | |
| **IsProd** | Character(1) | Es un Producto | Y |
| **IsWIP** | Character(1) | Es un Trabajo en Progreso (ej. Jarabe) | |
| **IsMatl** | Character(1) | Es Materia Prima | |
| **IsPal** | Character(1) | Es un Pallet | |
| **IsReuse** | Character(1) | Es Reutilizable (ej. Shell) | |
| **Ismake** | Character(1) | Es Producido | Y |
| **IsBuy** | Character(1) | Es Comprado | |
| **IsRemake** | Character(1) | Es Reacondicionamiento o Multipack | |
| **IsSell** | Character(1) | Se Vende al Cliente | |
| **BaseUoM** | Character(12) | Unidad de medida para conteo de inventario | CASE, BIB |

---
### IMAKEACTS.docx

Este objeto técnico registra los segmentos de ejecución de producción física reportados desde las líneas.

####  Propiedades de la Interfaz (Properties)
* **Parcel Type**: MAKEACTS.
* **Interface Table Name**: IMAKEACTS.

#### Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento `load_parcel`. | |
| **SegmentCD** | Character | Identificador único del segmento de producción (MakeID – Segment). | `9999-1` |
| **Shift** | Character | Identificador del turno de producción. | `001, 002 o 003` |
| **LineCd** | Character(25) | Identificador único de la línea de producción. | `THAI_PL-2` |
| **MakeItemCd** | Character(25) | Identificador único del ítem producido. | `501068` |
| **BOMverCd** | Character(25) | Identificador único de la lista de materiales (BOM). | `92001` |
| **RunFromTm** | DateTime | Fecha y hora de inicio de la corrida. | `11/20/2020 02:19` |
| **RunThruTm** | DateTime | Fecha y hora de fin de la corrida. | `11/21/2020 10:38` |
| **RunNetQty** | Float | Cantidad neta producida. | `21903` |
| **RunHrs** | Float | Horas totales de producción. | `32.32` |
| **AsOfStamp** | DateTime | Fecha y hora en que se registró el valor. | `11/21/2020 17:05` |
| **MakeInvStatus**| Character(16) | Estado de la corrida al momento del inventario. | `Scheduled, Running, Delivered, Cancelled` |
| **MakeCurrStatus**| Character(16) | Estado actual de la corrida de producción. | `Scheduled, Running, Delivered, Cancelled` |
| **RunGrossQty**| Float | Cantidad bruta total producida. | `21950` |

### MAKEBYSEGMENTS.docx

Este objeto técnico registra la programación de producción física por segmentos reportada al sistema.

#### Propiedades de la Interfaz (Properties)
* **Parcel Type**: MAKEBYSEGMENTS.
* **Interface Table Name**: XMAKESEGMENTS.

#### Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento `load_parcel`. | |
| **SegmentCD** | Character | Identificador único del segmento (MakeID – Segment). | `9999-1, 9999-2, etc.` |
| **Shift** | Character | Identificador del turno de producción. | `001, 002 or 003` |
| **Segment** | Number(10) | Identificador numérico del segmento. | `1, 2, 3, 4 . . . N` |
| **LocCd** | Character | Código de ubicación. | `92001` |
| **LineCd** | Character | Código de la línea de producción. | `7` |
| **ItemCd** | Character | Código del ítem. | `501316` |
| **RunFromTm** | DateTime | Fecha y hora de inicio programada. | `11/20/2020 2:19` |
| **RunThruTm** | DateTime | Fecha y hora de fin programada. | `11/21/2020 7:00` |
| **RunQty** | Number | Cantidad programada de la corrida. | `21903` |
| **RunHrs** | Number | Horas de producción estimadas. | `4.6` |
| **BoMVerCd** | Character | Código de versión de la lista de materiales. | `1` |
| **MakeId** | Number | Identificador único de corrida generado por el sistema. | `9999` |

### SHIPACTS.docx

Este objeto técnico registra la información de embarques reales (Actual Shippers).

####  Propiedades de la Interfaz (Properties)
* **Parcel Type**: SHIPACTS
* **Interface Table Name**: ISHIPACTS

####  Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento load_parcel | |
| **ShipHdrId** | Number(10) | ID generado para el encabezado de factura/transacción de embarque | 10000345 |
| **FrLocCd** | Character(25) | Identificador único del origen | 92001 |
| **ToLocCd** | Character(25) | Identificador único del destino | 92007 |
| **LoadTm** | DateTime | Hora de carga | 11/20/2020 02:38 |
| **DepartTm** | DateTime | Hora de salida de la ubicación de origen | 11/20/2020 03:00 |
| **DlvyTm** | DateTime | Hora de entrega/recepción | 11/21/2020 10:38 |
| **ItemCd** | Character(25) | Identificador único del ítem | 500248 |
| **LoadQty** | Float | Cantidad cargada | 5280 |
| **RcvdQty** | Float | Cantidad recibida | 5280 |
| **ShipInvStatus** | Character(16) | Estado de la carga al momento del inventario | Schd, Load, Rcvd, Canc |
| **ShipCurrStatus** | Character(16) | Estado actual de la carga | Schd, Load, Rcvd, Canc |
| **InvLotId** | Number(10) | ID generado para un lote de corrida de producción | 193059 |


### SHIPSCHD.docx 
Definición de Embarques Programados (SHIPSCHD)

Este objeto técnico registra la programación de embarques (Scheduled 
Shippers).

#### Propiedades de la Interfaz (Properties)
* **Parcel Type**: SHIPSCHD
* **Interface Table Name**: ISHIPSCHD

#### Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento load_parcel | |
| **FrLocCd** | Character(25) | Identificador único del origen | 92001 |
| **ToLocCd** | Character(160) | Identificador único del destino | 92007 |
| **LoadTm** | DateTime | Hora de carga | 11/20/2020 02:38 |
| **DlvyTm** | DateTime | Hora de recepción | 11/21/2020 10:38 |
| **ItemCd** | Character(160) | Identificador único del ítem | 500248 |
| **ShipQty** | Float | Cantidad base | 5280 |
| **PalItemCd** | Character(160) | Código de pallet | 0001 |
| **PalQty** | Float | Cantidad de pallets | 24 |
| **ShipInvStatus** | Character(16) | Estados válidos: Schd, Load, Dlvd, Canc | Schd |
| **ShipCurrStatus** | Character(16) | Estados válidos: Schd, Load, Dlvd, Canc | Schd |
| **ShipType** | Character(16) | Tipos: Deploy, Cross-Deploy, Transfer, Buy, Purchase, Sale | Deploy |
| **LastExpStamp** | Date/Time | Sello de tiempo de última exportación | 11/21/2020 17:00 |
| **ShipHdrId** | Number(10) | Identificador de encabezado de embarque generado | 710952 |
| **LastImpStamp** | Date/Time | Sello de tiempo de última importación | 11/22/2020 07:00 |


### IVARIETYS.docx
Definición de Variedades (IVARIETYS)

Una variedad, o marca-sabor, es un atributo de un producto. El nombre corto de la variedad debe contener dos elementos, por ejemplo, la marca (**Brand**) y el sabor (**Flavor**).

####  Propiedades de la Interfaz (Properties)
* **Parcel Type**: VARIETYS
* **Interface Table Name**: IVARIETYS

####  Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento `load_parcel` | |
| **VarietyCd** | Character(25) | Identificador alfanumérico único | 02 |
| **Variety** | Character(25) | Nombre corto único | B_Lem_Soda |
| **VarietyNm** | Character(100)| Nombre largo | Bill’s Lemon Soda |
| **VarietyTag1**| Character(64) | Tipo | CSD |
| **VarietySeq** | Character(25) | Secuencia de variedades en editores | 034 |


## EfletexIA

### T1 

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


#### WS BM - Efletex(Anuncios Regulares).docx


```bash
COMPROBAR STATUS DE ENVIO
Url: status-envio
Método: HTTP REQUEST | GET

Parámetros
Tipo de dato
Datos
tokenapi
string
proporcionado por Efletex
clienteid
int
id del cliente en Efletex
fecha
date
formato yyyy-mm-dd


{
"data": [
{
"envioid": 1598, "status": "RESERVADO",
"clienteid": 626,
"transportistaid": 214, "transportista_codigo": "", "fecha": "2017-08-04 12:04:27",
"precio": "900",
"carga_desde": "2017-08-14", "carga_hasta": null, "entrega_desde": "2017-08-15", "entrega_hasta": null
}, {
"envioid": 1599, "status": "EXPIRADO", "clienteid": 626, "transportistaid": "",
"transportista_codigo": "", "fecha": ""
},

],
"status": "success", "results": 1,
"message": "Lista de envios con status reservado y eliminado"
}







PUBLICAR ENVIO


Descripción: este servicio se utiliza para crear el registro con los datos del envío, para después ser procesado en Efletex. Debe enviarse la información del o los pedidos que conforman este envío (los datos del cliente, los litros y pesos (kg) de los pedidos).

URL: apiV2/envios
METODO: POST


Parametros:
Tipo Dato
Datos
tokenapi
string
proporcionado por efletex
clienteid
int
id del cliente en efletex
codigo_envio
string
id del envio en el ERP
fecha_carga_desde
date
formato yyyy-mm-dd
fecha_carga_hasta
date
formato yyyy-mm-dd
fecha_entrega_desde
date
formato yyyy-mm-dd
fecha_entrega_hasta
date
formato yyyy-mm-dd
hora_carga_desde
time
formato hh:mm:ss
hora_carga_hasta
time
formato hh:mm:ss
hora_carga_desde
time
formato hh:mm:ss
hora_carga_hasta
time
formato hh:mm:ss
fecha_expiracion
date
formato yyyy-mm-dd
hora_expiracion
time
formato hh:mm:ss
estado_carga
ciudad_carga direccion_carga ubicacion_carga contacto_carga telefono_carga lugar_carga otro_lugar_carga estado_entrega ciudad_entrega direccion_entrega ubicacion_entrega contacto_entrega telefono_entrega lugar_entrega
otro_lugar_entrega
int
string string coords string numeric int string int string string coords string string int
string
id del estado/depto.
formato latitud,longitud id de lugares efletex
id del estado/depto..
formato latitud,longitud id de lugares efletex




artículos
array
contiene artículos en formato json
titulo
string


tipo_precio
int
1=fijo,2=libre,3=mixto
tipo_envio
int
0=publico,1=privado
grupoid
int
id del grupo del cliente efletex
servicioid
int
id del servicio efletex
tipovehiculoid
int
id del tipo de vehículo efletex
metodopagoid
int
id del método de pago efletex
precio_envio
float


porcentaje_inicial
float
mayor a 0 menor a 100
condiciones_pago
string


transportistas
array
códigos de transportistas
elevador_carga
int
0=false,1=true
cargar_interior
int
0=false,1=true
llamar_antes_entrega
int
0=false,1=true
elevador_entrega
int
0=false,1=true
entrega_interior
int
0=false,1=true
proteccion_frio
int
0=false,1=true
clasificar_separar
int
0=false,1=true
persona_invidente
int
0=false,1=true
solo_comunidad
int
0=false,1=true
mostrar_ofertantes
int
0=false,1=true
codigo_cliente_erp
string
código del cliente en el erp
nombre_cliente
string


razon_social_cliente
string


canal_cliente
string


codigo_pedido
array
info de pedidos
fecha_erp
date
formato yyyy-mm-dd hh:ii:ss





Parámetro: transportistas
Tipo: array
Contiene los códigos de los transportistas separados por comas. Previamente deben estar relacionados con el cliente.
transportistas = codigo1,codigo2,cod….;

Parámetro: artículos
Tipo: array
Contiene datos json de los artículos a publicar. articulos =
{“unidadid”:””,”peso”:””,”unidad_peso”:””,”cantidad”:””,”largo”:””,”alto”:””,”ancho”:””,”unidad_ medida”:””,”descripcion”:””,”apilable”:””,”peligroso”:””,”perecedero”:””}


Atributos
Tipo de Dato
Datos
unidadid
int
id de la unidad en efletex
peso
float


unidad_peso
string
cadenas permitidas Kg, Lb, Tn
cantidad
int
numero de unidades
largo
float
dimensión articulo
alto
float
dimensión articulo
ancho
float
dimensión articulo
unidad_medida
string
cadenas permitidas cm,m,in
descripcion
string


apilable
int
0=false,1=true
peligroso
int
0=false,1=true
perecedero
int
0=false,1=true



Parámetro: codigo_pedido
Tipo: array
Contiene datos json de los pedidos que conforman el anuncio codigo_pedido = {“codigo”:””,”litros”:””,”peso”:””,”fecha”:””,”hora”:””}

Atributos
Tipo de Dato
Datos
codigo
string
codigo del pedido
litros
float
total de litros del pedido
peso
float
total de kg del pedido
fecha
date
formato yyyy-mm-dd
hora
time
formato hh:ii:ss



Consideraciones
otro_lugar_carga es obligatorio si lugar_carga=6 otro_lugar_entrega es obligatorio si lugar_entrega=6 grupoid es obligatorio si tipo_envio=1
transportistas es obligatorio si desea hacer envios dirigidos.
metodopagoid, tipovehiculoid, servicioid, condicionespago pueden ir vacíos si no va a definirlos en el envío.


Ejemplo de llamada:
https://efletex.com/apiV2/envios?tokenapi=valor-token&clienteid=idcliente-proporcionado&codigo_envio=12345&fecha_carga_desde=2019-05-14&fecha_carga_hasta=2019-05-14&fecha_entrega_desde=2019-05-16&fecha_entrega_hasta=2019-05-16&hora_carga_desde=13:00:00&hora_carga_hasta=23:00:00&hora_entrega_desde=07:00:00&h ora_entrega_hasta=16:00:00&fecha_expiracion=2019-05-14&hora_expiracion=12:30:00&estado_carga=2431&ciudad_carga= TUXTLA GUTIERREZ&direccion_carga=LA SALLE 323 &ubicacion_carga= 16.7401171,-93.0926997&contacto_carga=SUPERVISOR DE TRANSPORTE&telefono_carga=9611234567&lugar_carga=2&estado_entrega=2431&ciudad_entre ga= TUXTLA GUTIERREZ&direccion_entrega=5 de mayo &ubicacion_entrega= 16.752341, - 93.106323&contacto_entrega=CLIENTE&telefono_entrega=9611234567&lugar_entrega=2&articul os=[{"unidadid":"29","peso":"30","unidad_peso":"Tn","cantidad":"1","largo":"13.5","alto":"2.6","a ncho":"3.6","unidad_medida":"m","descripcion":"documentos vigentes de la unidad","apilable":"0","peligroso":"0","perecedero":"0"}]&titulo=VIAJE TUXTLA – 5 DE MAYO &tipo_precio=1&tipo_envio=1&grupoid=23&servicioid=1&tipovehiculoid=8&metodopagoid=2&pr ecio_envio=3840&porcentaje_inicial=0&condiciones_pago=PAGO 15 DIAS DESPUES DE ENTREGADA LA
FACTURA&elevador_carga=0&cargar_interior=0&llamar_antes_entrega=0&elevador_entrega=0& entrega_interior=0&proteccion_frio=0&clasificar_separar=0&persona_invidente=0&solo_comunid ad=1&mostrar_ofertantes=0&transportista=[]&codigo_pedido=[{"codigo":"OC324","litros":23456, "peso":23456,"fecha":"2019-07-20","hora":"11:00:00"}]&codigo_cliente_erp=04567&nombre_cliente=TEST&canal_cliente=TESTIN G&razon_social_cliente=TEST EFLETEX&fecha_erp=2019-06-15 14:06:40

Ejemplo de respuesta satisfactoria:

{
"data": { "envioid": null,
"status": "PENDIENTE DE PUBLICAR"
},
"status": "success",
"results": "1",
"message": "Datos Recibidos"
}

Ejemplo de respuesta de error:

{
"status": "error",
"results": "0",
"message": "mensaje de error"
}




DOCUMENTACION ENVIO
Descripción: se envían los datos de las guías de remisión, con la información general del cliente y transportista.

URL: apiV2/documentacion-envio
Metodo: POST
Envío de datos por body


Parametros:
Tipo Dato
Datos
tokenapi
string
proporcionado por efletex
data
array
array con estructura json


Parametros de la estructura data


Campo
Tipo Dato
Datos
envioid
int
id del envio (ref Efletex)
clienteid
int
id del cliente de Efletex
tipo_documento
string
OC=Orden Carga, G= Guia
folio_orden_carga
string
seriado de la orden de carga
codigoFlete
string
codigo del envio en el ERP
fecha_orden_carga
date time
formato yyyy-mm-dd hh:ii:ss
status_orden_carga
string
liquidada o no liquidada, cancelada
folio_guia
string
seriado de la guía
fecha_guia
date time
formato yyyy-mm-dd hh:ii:ss
litros
float
total de litros de la guía
peso
float
total de kg de la guía
status_guia
string
liquidada o no liquidada, cancelada
tipo_vehiculo
string
codigo + descripción (cod,descr)
codigo_cliente
string
codigo del cliente en el ERP
salida_guia
string
procedimiento de la guía
codigo_transportista
string
codigo del trt en el ERP
placa
string
placa del vehiculo
chofer
string
codigo del conductor en el ERP
tarimas
string
numero de palets
calle_entrega
string
calle del punto de entrega
ciudad_entrega
string
ciudad del punto de entrega
estado_entrega
string
estado del punto de entrega
capacidad_codigo
string
codigo de la capacidad del vehiculo
capacidad_nombre

Ejemplo llamada
string
descripción de la capacidad


{"tokenapi":"token-proporcionado","data":[{"fecha_orden_carga":"2019-07-09 09:32:15","codigoFlete":"00300001FLT0000010311","tipo_documento":"OC","status_orden_carga ":"ACTIVO","envioid":"12345","clienteid":idproporcionado,"folio_orden_carga":"GRA 0000572227"}]}


{"tokenapi":" token-proporcionado ","data":[{"codigoFlete":"00300001FLT0000010311","estado_entrega":"TABASCO ","chofer":1702435,"capacidad_nombre":"SENCILLO	","codigo_cliente": idproporcionado,"tarimas":22,"envioid":"12345","folio_orden_carga":"GRA 0000572227","calle_entrega":"ANACLETO CANABAL 1A
SECCION","ciudad_entrega":"CENTRO","litros":21348.54,"peso":16317.171999999999,"status_gui a":"ACTIVO","tipo_vehiculo":"003,TRAILER","tipo_documento":"G","folio_guia":"HP-0000000000229475","fecha_guia":"2019-07-09
12:25:30.063","precinto":"0136344","codigo_transportista":1589779,"capacidad_codigo":"001"," placa":"52AF1B ","clienteid":1495,"salida_guia":"EMPRESA "}]}




Ejemplo respuesta satisfactoria:
{
"status": "success", "errors": "array-errores",
"inserts": "numero-insertados", "message": "Consumo Exitoso"
}


Ejemplo error:
{
"status": "error", "errors": "array-errores",
"inserts": "numero-insertados",
"message": "Ocurrio un error en el WS documentacionEnvio, code 1"
}




```





### T2

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


#### SP BM Relacionados.docx

**SP BM Relacionado**

**Envio de Pedidos y Clientes**  
Store procedure que envía información de los pedidos hacia EfletexIA y tambien incluye lista de clientes programados en cada viaje.

**Stored Procedure: COM_PREPARAR_CARGA_PEDIDO_PLINT**

```sql
ALTER PROCEDURE [dbo].[COM_PREPARAR_CARGA_PEDIDO_PLINT]
@COMPANIA CHAR(4),
@SUCURSAL CHAR(4),
@EMISOR CHAR(4),
@ZONA NVARCHAR(max),
@ID INT

AS
BEGIN

    --EXEC [COM_PREPARAR_CARGA_PEDIDO_PLINT] '0076','08','02','31000'
    SET NOCOUNT ON;

    DECLARE @V_XML XML;
    DECLARE @v_eXML varchar (max);
    DECLARE @Pais char(2);

    -- CREAMOS TEMPORAL CON LAS ZONAS A BUSCAR
    CREATE TABLE #TMP_ZONAS (
        ZONA INT
    )
    INSERT INTO #TMP_ZONAS(ZONA)
    SELECT * FROM dbo.Split(@ZONA, ',')

    DECLARE @FECDISTRIB INT, @FECPREVTA INT, @EFFACTUR CHAR(3), @EPASSTOCK CHAR(3)

    SELECT @FECDISTRIB=FECDISTRIB, @FECPREVTA=FECPREVTA
    FROM MEMIS01F WITH (NOLOCK)
    WHERE COMPANIA=@COMPANIA AND SUCURSAL=@SUCURSAL AND EMISOR=@EMISOR

    --set @fecprevta=dbo.fc_integerdate('04/02/2010')
    --set @fecdistrib=dbo.fc_integerdate('05/02/2010')

    SELECT @EFFACTUR=EFFACTUR, @EPASSTOCK = EPASSTOCK
    FROM MPADIS1F WITH (NOLOCK)
    WHERE COMPANIA=@COMPANIA

    ---------------------------------------------------------------------------
    -- Se realiza envio de data de clientes para los pedidos seleccionados --
    ---------------------------------------------------------------------------
    DECLARE @CTE_X_PEDI INT, @CTE_X_INTE INT

    SELECT clienteID, CODFVTA3
    INTO #CLIENTES_PEDIDO
    FROM (
        SELECT DISTINCT A.CLIENTE AS clienteID, E.CODFVTA3
        FROM TPEDID2F A WITH (NOLOCK)
        INNER JOIN MARTIC1F B WITH (NOLOCK) ON A.COMPANIA=B.COMPANIA AND A.ARTICULO=B.ARTICULO
        INNER JOIN TPEDID1F E WITH (NOLOCK) ON A.COMPANIA=E.COMPANIA AND 
            A.SUCURSAL=E.SUCURSAL AND A.TIPO=E.TIPO AND A.NRODOC=E.NRODOC
            A.SUCURSAL=E.SUCURSAL AND A.EMISOR=E.EMISOR AND 
            A.DOCUPEDIDO=E.DOCUPEDIDO AND 
            A.NROPEDIDO=E.NROPEDIDO AND E.FECPEDIDO=@FECPREVTA
        LEFT JOIN MCLIEN4F D WITH (NOLOCK) ON A.COMPANIA=D.COMPANIA AND 
            A.SUCURSAL=D.SUCURSAL AND A.CLIENTE=D.CLIENTE AND E.CODFVTA3=D.CODFVTA3
        INNER JOIN MLINEA1F F WITH (NOLOCK) ON B.COMPANIA=F.COMPANIA AND 
            B.LINEA=F.LINEA AND F.FLGLINEA='Te'
        INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
        WHERE A.COMPANIA=@COMPANIA and A.SUCURSAL=@SUCURSAL and A.EMISOR=@EMISOR and 
        a.stspederr='N' AND
            --A.ZONADIST=ISNULL(@ZONA,A.ZONADIST) and
            A.FLGASIGNAC='S' AND COALESCE(A.DOCUCOMALM,'')='' AND
            COALESCE(A.NROCOMALM,'')='' AND A.STSPEDIDO=@EPASSTOCK
            AND ISNULL(E.ORIGPEDIDO, '') NOT IN ('011')
        UNION ALL
        SELECT DISTINCT A.CLIENTE AS clienteID, E.CODFVTA3
        FROM TPEDID2F A WITH (NOLOCK)
        INNER JOIN MARTIC1F B WITH (NOLOCK) ON A.COMPANIA=B.COMPANIA AND 
            A.ARTICULO=B.ARTICULO
        INNER JOIN TPEDID1F E WITH (NOLOCK) ON A.COMPANIA=E.COMPANIA AND 
            A.SUCURSAL=E.SUCURSAL AND A.EMISOR=E.EMISOR AND 
            A.DOCUPEDIDO=E.DOCUPEDIDO AND 
            A.NROPEDIDO=E.NROPEDIDO 
            AND E.FECENTREGA = @FECDISTRIB
        LEFT JOIN MCLIEN4F D WITH (NOLOCK) ON A.COMPANIA=D.COMPANIA AND 
            A.SUCURSAL=D.SUCURSAL AND A.CLIENTE=D.CLIENTE AND E.CODFVTA3=D.CODFVTA3
        INNER JOIN MLINEA1F F WITH (NOLOCK) ON B.COMPANIA=F.COMPANIA AND 
            B.LINEA=F.LINEA AND F.FLGLINEA='Te'
        INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
        WHERE A.COMPANIA=@COMPANIA and A.SUCURSAL=@SUCURSAL and A.EMISOR=@EMISOR and 
        a.stspederr='N' AND
            --A.ZONADIST=ISNULL(@ZONA,A.ZONADIST) and
            A.FLGASIGNAC='S' AND COALESCE(A.DOCUCOMALM,'')='' AND
            COALESCE(A.NROCOMALM,'')='' AND A.STSPEDIDO=@EPASSTOCK
            AND E.ORIGPEDIDO = '011') AS A

    SELECT DISTINCT clienteID, CODFVTA3
    INTO #CLIENTES_INTEGRA
    FROM #CLIENTES_PEDIDO A
    /* Se elimina filtro para poder reenviar los clientes no importando que ya se hallan enviado
    WHERE NOT EXISTS (SELECT 1
                      FROM MCLIEN22F C WITH (NOLOCK)
                      WHERE C.COMPANIA = @COMPANIA
                      AND C.CLIENTE = A.clienteID
                      AND C.FECCREACIO = dbo.FC_INTEGERDATE(GETDATE())
                      AND C.TIPOINTE = 'C'
                      AND C.ESTAINTE = 'I')*/

    --SELECT @CTE_X_PEDI = COUNT(*) FROM #CLIENTES_PEDIDO
    SELECT @CTE_X_INTE = COUNT(*) FROM #CLIENTES_INTEGRA

    IF @CTE_X_INTE > 0
    BEGIN

        DECLARE @CODLETR CHAR(2)

        --Obtener codigo pais
        SELECT @CODLETR = B.CODLETR
        FROM MCOMPA1F A WITH (NOLOCK)
        INNER JOIN BUBIGE1F B WITH (NOLOCK) ON A.PAIS = B.PAIS
        WHERE A.COMPANIA = @COMPANIA

        INSERT INTO TPLINT1F ([FCREACION], [ESTADO], [ROOTKEY], [SUCURSAL])
        VALUES (GETDATE(), 0, 'Clientes', @SUCURSAL)

        DECLARE @v_ID INT = 0;

        SELECT TOP 1 @v_ID = ID
        FROM TPLINT1F WITH (NOLOCK)
        WHERE ROOTKEY = 'Clientes'
          AND SUCURSAL = @SUCURSAL
        ORDER BY ID DESC;

        DECLARE @XmlCliente xml
        SET @XmlCliente = (
            SELECT 
                @COMPANIA AS compania,
                @v_ID AS idTableBM,
                -- Esto es para F2
                'CLIENTES' AS tipo,
                (
                SELECT
                    A.CLIENTE AS clienteID,
                    LTRIM(RTRIM(SUBSTRING(A.NOMCLIENTE, 1, 60))) AS nombre,
                    LTRIM(RTRIM(DIRDETCLCL)) AS direccion,
                    @CODLETR AS pais,
                    CAST(ISNULL(B.COORDY, 0.0) AS DECIMAL(18,6)) AS latitude,
                    CAST(ISNULL(B.COORDX, 0.0) AS DECIMAL(18,6)) AS longitude,
                    D.RUTA AS rutaID,
                    E.ZONADIST AS zonaID,
                    D.MODULO AS moduloID,
                    CONCAT(
                        CASE WHEN ISNULL(C.FLGLUNES, 'N') = 'S' THEN 'L' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGMARTES, 'N') = 'S' THEN 'M' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGMIERCOLES, 'N') = 'S' THEN 'R' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGJUEVES, 'N') = 'S' THEN 'J' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGVIERNES, 'N') = 'S' THEN 'V' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGSABADO, 'N') = 'S' THEN 'S' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGDOMINGO, 'N') = 'S' THEN 'D' ELSE '' END
                    ) AS diasEnvio,
                    LTRIM(RTRIM(A.CANAL)) AS codigoCanal,
                    LTRIM(RTRIM(H.DESCRIPCION)) AS canal,
                    LTRIM(RTRIM(A.TLFCLIENTE)) AS telefono,
                    LTRIM(RTRIM(A.GIRONEGOCI)) AS codigoGiro,
                    LTRIM(RTRIM(I.GIRDNOM)) AS giro,
                    LTRIM(RTRIM(A.SUBGIROVS)) AS codigoSubGiro,
                    LTRIM(RTRIM(J.DESCSGIRO)) AS subGiro,
                    LTRIM(RTRIM(A.RUCCLIENTE)) AS RUC,
                    LTRIM(RTRIM(ISNULL(K.EMAIL, ''))) AS email
                FROM dbo.MCLIEN1F (NOLOCK) A
                LEFT OUTER JOIN dbo.MCLIEN4F (NOLOCK) B ON A.COMPANIA = ...
                B.COMPANIA AND A.SUCURSAL = B.SUCURSAL AND A.CLIENTE = B.CLIENTE
                LEFT OUTER JOIN dbo.MCLIEN11F (NOLOCK) C ON A.COMPANIA = 
                    C.COMPANIA AND A.CLIENTE = C.CLIENTE
                INNER JOIN dbo.MESTDI4F (NOLOCK) D ON A.COMPANIA = 
                    D.COMPANIA AND A.SUCURSAL = D.SUCURSAL AND B.MODULO = D.MODULO AND B.CODFVTA3 = D.CODFVTA3
                INNER JOIN dbo.MESTDI3F (NOLOCK) E ON A.COMPANIA = 
                    E.COMPANIA AND A.SUCURSAL = E.SUCURSAL AND D.RUTA = E.RUTA
                INNER JOIN dbo.MESTDI2F (NOLOCK) F ON A.COMPANIA = 
                    F.COMPANIA AND A.SUCURSAL = F.SUCURSAL AND E.ZONADIST = F.ZONADIST
                LEFT OUTER JOIN dbo.MPERSO1F (NOLOCK) G ON E.COMPANIA = 
                    G.COMPANIA AND E.VENDEDOR = G.PERSONA
                INNER JOIN dbo.TRELCONS1F (NOLOCK) T ON A.COMPANIA = 
                    T.COMPANIA AND A.SUBGIROVS = T.SUBGIRO
                INNER JOIN dbo.MCANDIST (NOLOCK) H ON A.COMPANIA = 
                    H.COMPANIA AND T.CANAL = H.CANAL
                INNER JOIN dbo.BGIRO1F (NOLOCK) I ON A.COMPANIA = 
                    I.COMPANIA AND T.GIRO = I.GIROEMPRES
                INNER JOIN dbo.BSGIRO1F (NOLOCK) J ON A.COMPANIA = 
                    J.COMPANIA AND A.SUBGIROVS = J.SUBGIRO
                INNER JOIN dbo.MPERSO1F (NOLOCK) K ON K.COMPANIA = 
                    A.COMPANIA AND K.PERSONA = A.CLIENTE
                INNER JOIN #CLIENTES_INTEGRA L ON A.CLIENTE = L.clienteID 
                    AND B.CODFVTA3 = L.CODFVTA3
                WHERE A.COMPANIA = @COMPANIA
                  AND A.SUCURSAL = @SUCURSAL
                FOR XML PATH ('cliente'), TYPE
                )
            FOR XML PATH (''), ROOT('clientes')
        )

        DECLARE @xmlcharCliente VARCHAR(MAX)
        SET @xmlcharCliente = CAST(@XmlCliente AS VARCHAR(MAX))

        UPDATE TPLINT1F
        SET DATA = @xmlcharCliente
        WHERE ID = @v_ID;

        -- Esto es para F2
        EXEC COM_PLINT_CONSUMO_AWS 'M', @COMPANIA, @SUCURSAL, @xmlcharCliente
        --EXEC COM_PLINT_CONSUMO_AWS 'C', @COMPANIA, @SUCURSAL, @xmlcharCliente

        -- Se inserta Registro de Log de Integración
        INSERT INTO MCLIEN22F
        SELECT @COMPANIA, clienteID, 'C', 'I', dbo.FC_INTEGERDATE(GETDATE()), 
            dbo.FC_HORA(GETDATE()), 'SYSTEM', dbo.FC_INTEGERDATE(GETDATE()), dbo.FC_HORA(GETDATE()), 
            'SYSTEM'
        FROM #CLIENTES_INTEGRA A
        WHERE NOT EXISTS (SELECT * FROM MCLIEN22F C WHERE C.COMPANIA = @COMPANIA AND 
            C.CLIENTE = A.clienteID AND C.TIPOINTE = 'C' AND C.FECCREACIO = 
            dbo.FC_INTEGERDATE(GETDATE()))

        -- Se actualiza registro de Integración Pendiente
        UPDATE A
        SET A.ESTAINTE = 'I'
        FROM MCLIEN22F A
        INNER JOIN #CLIENTES_INTEGRA B ON A.CLIENTE = B.clienteID
        AND A.ESTAINTE = 'P'
    END
------------------------------------------------------------------------------------------
--                                                             FIN INTEGRACION CLIENTES --
------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------
    -- SE REALIZA CAMBIO DE PROCEDURE PARA MANEJAR UN MAXIMO DE 1000 PEDIDOS - CLIENTE POR ENVIO,
    -- PARA EVITAR EL TAMAÑO MAXIMO DE DATA POR ENVIAR EN AWS
    ------------------------------------------------------------------------------------------
    
    SELECT ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS ROWNUM, a.COMPANIA, a.SUCURSAL, 
    a.CLIENTE, a.DOCUPEDIDO, a.NROPEDIDO
    INTO #DATA_PEDIDOS
    FROM DBO.TPGVEH1F (NOLOCK) a
        INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
        INNER JOIN DBO.TPEDID1F (NOLOCK) d ON a.compania = d.compania and a.sucursal = 
    d.sucursal and a.docupedido = d.docupedido and a.nropedido = d.nropedido
    WHERE a.COMPANIA = @COMPANIA
        AND a.SUCURSAL = @SUCURSAL
        AND ISNULL(a.DOCUCOMALM, '')=''

    DECLARE @NTOTAL INT,
            @NITERA INT,
            @NIDX INT = 0,
            @OPSENVIO VARCHAR(500) = ''

    DECLARE @ID_LOTE INT ;

    SELECT @NTOTAL = COUNT(*) FROM #DATA_PEDIDOS
    SELECT @NITERA = @NTOTAL / 1000

    WHILE (@NIDX * 1000 < @NTOTAL)
    BEGIN

        --INSERTAR AL INBOX PARA GENERAR ID
        INSERT INTO TPLINT1F ([FCREACION], [ESTADO], [ROOTKEY], [SUCURSAL])
        VALUES (GETDATE(), 0, 'Pedidos', @SUCURSAL)

        -- OBTENEMOS EL ID CREADO
        SELECT TOP 1 @ID_LOTE = ID
        FROM TPLINT1F
        WHERE ROOTKEY = 'Pedidos'
            AND SUCURSAL = @SUCURSAL
        ORDER BY ID DESC --SET @ID_LOTE = isnull((SELECT top 1 ID_LOTE FROM TPGVEH2F 
    order by ID_LOTE desc),0) + 1

        SET @V_XML = (
            SELECT
                @COMPANIA AS compania,
                LTRIM(RTRIM(@SUCURSAL)) AS sucursal,
                @ID_LOTE AS idTableBM,
                (
                    SELECT
                        CONCAT(LTRIM(RTRIM(A.DOCUPEDIDO)), '-', 
                CAST(A.NROPEDIDO AS VARCHAR), '-', CAST(A.CLIENTE AS VARCHAR)) AS ID,
                        a.CLIENTE AS clienteID,
                        CAST((
                            SELECT
                                SUM(CAST(ISNULL(D.QCAJASIGP + 
                (D.QBOTASIGP / E.QCONTENIDO), 0) AS float)) AS cajas
                            FROM DBO.TPEDID2F (NOLOCK) D
                            INNER JOIN DBO.MARTIC1F (NOLOCK) E ON 
                D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON 
                E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                            AND D.SUCURSAL = a.SUCURSAL
                            AND D.DOCUPEDIDO = A.DOCUPEDIDO
                            AND D.NROPEDIDO = A.NROPEDIDO
                            AND D.CLIENTE = A.CLIENTE
                        ) AS varchar) AS cajas,
                        CAST((
                            SELECT
                                SUM(CAST(ISNULL(E.QPESO * 
                ISNULL(D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO), 0) ,0) AS float)) AS pesoTotal
                            FROM DBO.TPEDID2F (NOLOCK) D
                            INNER JOIN DBO.MARTIC1F (NOLOCK) E ON 
                D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON 
                E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                            AND D.SUCURSAL = a.SUCURSAL
                            AND D.DOCUPEDIDO = A.DOCUPEDIDO
                            AND D.NROPEDIDO = A.NROPEDIDO
                            AND D.CLIENTE = A.CLIENTE
                        ) AS varchar) AS peso,
                        CAST((
                            SELECT
                                SUM(CAST(ISNULL(E.QTOTAL * 
                ISNULL(D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0), 0) AS float)) AS volumenTotal
                            FROM DBO.TPEDID2F (NOLOCK) D
                            INNER JOIN DBO.MARTIC1F (NOLOCK) E ON 
                D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON 
                E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                            AND D.SUCURSAL = a.SUCURSAL
                            AND D.DOCUPEDIDO = A.DOCUPEDIDO
                            AND D.NROPEDIDO = A.NROPEDIDO
                            AND D.CLIENTE = A.CLIENTE
                        ) AS varchar) AS volumen,
                        'Venta' as tipoPedido,
                        CASE WHEN ISNULL(d.FECENTREGA, 0) > 0 
                            THEN CONVERT(date, dbo.FC_FECHA(d.FECENTREGA))
                            ELSE CONVERT(date, DATEADD(DAY, +1, GETDATE()))
                        END AS fechaEnvio,
                        (
                            SELECT
                                CAST(D.ARTICULO AS VARCHAR) AS articuloID,
                                LTRIM(RTRIM(E.DESCRIPI1)) AS articuloDescripcion,
                                CAST(ISNULL(D.QCAJASIGP, 0) AS DECIMAL(10,0)) AS cajas,
                                CAST(ISNULL(D.QBOTASIGP, 0) AS DECIMAL(10,0)) AS unidades,
                                CAST(CAST(ISNULL(E.QPESO * 
                ISNULL(D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO), 0) ,0) AS float) AS VARCHAR) AS pesoTotal,
                                CAST(CAST(ISNULL(E.QTOTAL * 
                ISNULL(D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0), 0) AS float) AS VARCHAR) AS volumenTotal,
                                CAST(CAST(ISNULL(E.QPESO * 
                ISNULL(D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO), 0) ,0) AS float) AS VARCHAR) AS peso,
                                CAST(CAST(ISNULL(E.QTOTAL * 
                ISNULL(D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0), 0) AS float) AS VARCHAR) AS volumen,
                                CASE D.PROCPEDIDO WHEN '003' THEN 
                                'Venta' WHEN '006' THEN 'Bonificación' ELSE 'Por Procesar' END as procedimientoDescripcion,
                                CAST(ISNULL(E.QCONTENIDO, 0) AS DECIMAL(10,0)) AS qContenido,
                                CAST(ISNULL((D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0) AS DECIMAL(10,0)) AS totalBotellas,
                                D.IDREGLA as codPromocion
                            FROM DBO.TPEDID2F D WITH (NOLOCK)
                            INNER JOIN DBO.MARTIC1F E WITH (NOLOCK) ON D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                                AND D.SUCURSAL = a.SUCURSAL
                                AND D.DOCUPEDIDO = A.DOCUPEDIDO
                                AND D.NROPEDIDO = A.NROPEDIDO
                                AND D.CLIENTE = A.CLIENTE
                                AND (D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO)) > 0
                                -- Se omite validacion por procedimiento
                                --AND D.PROCPEDIDO IN ('003', '006')
                            ORDER BY D.IDREGLA, D.PROCPEDIDO
                            FOR XML path('pedidoDetalle'), type
                        )
                    FROM DBO.TPGVEH1F (NOLOCK) a
                    INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
                    INNER JOIN DBO.TPEDID1F (NOLOCK) d ON a.compania = d.compania and a.sucursal = d.sucursal and a.docupedido = d.docupedido and a.nropedido = d.nropedido
                    INNER JOIN #DATA_PEDIDOS e ON a.COMPANIA = e.COMPANIA AND a.SUCURSAL = e.SUCURSAL and a.CLIENTE = e.CLIENTE and a.DOCUPEDIDO = e.DOCUPEDIDO and a.NROPEDIDO = e.NROPEDIDO
                    WHERE a.COMPANIA = @COMPANIA
                        AND a.SUCURSAL = @SUCURSAL
                        AND ISNULL(a.DOCUCOMALM, '') = ''
                        AND e.ROWNUM BETWEEN (@NIDX * 1000 + 1) AND (@NIDX * 1000 + 1000)
                        -- Se agrega filtrado para validar que no se agreguen cabeceras que no tienen detalles
                        AND EXISTS (SELECT 1 
                                    FROM dbo.TPEDID2F Z WITH (NOLOCK)
                                    INNER JOIN DBO.MARTIC1F Y WITH (NOLOCK) ON Z.COMPANIA = Y.COMPANIA AND Z.ARTICULO = Y.ARTICULO
                                    INNER JOIN dbo.MLINEA1F X WITH (NOLOCK) ON Y.COMPANIA = X.COMPANIA AND Y.LINEA = X.LINEA AND X.FLGLINEA = 'Te'
                                    WHERE Z.COMPANIA = A.COMPANIA
                                        AND Z.SUCURSAL = A.SUCURSAL
                                        AND Z.DOCUPEDIDO = A.DOCUPEDIDO
                                        AND Z.NROPEDIDO = A.NROPEDIDO
                                        AND Z.CLIENTE = A.CLIENTE
                                        AND (Z.QCAJASIGP + (Z.QBOTASIGP / Y.QCONTENIDO)) > 0
                                        -- Se omite validacion por procedimiento
                                        --AND Z.PROCPEDIDO IN ('003', '006')
                                    )
                    FOR XML path('pedido'), type
                )
            FROM DBO.TCOMPA2F (NOLOCK)
            WHERE COMPANIA=@COMPANIA AND SUCURSAL=@SUCURSAL
            FOR XML PATH ('pedidos'), type
        )
        SET @v_eXML = cast(@V_XML as varchar(max));    ---CONVERT(@V_XML, varchar(max));

        -- ACTUALIZAMOS EL REGISTRO CREADO CON LA DATA QUE SE ENVIA
        UPDATE TPLINT1F
        SET DATA = @v_eXML
        WHERE ROOTKEY = 'Pedidos' AND ID = @ID_LOTE
        AND SUCURSAL = @SUCURSAL

        EXEC [COM_PLINT_INTEGRATION_CONSUMO_AWS] 'ROADNET', @Pais, @COMPANIA, @ID_LOTE, @v_eXML;

        SET @OPSENVIO += CASE WHEN LEN(LTRIM(RTRIM(@OPSENVIO))) = 0 THEN '' ELSE ',' END + CAST(@ID_LOTE AS VARCHAR)

        SET @NIDX += 1
    END

    DECLARE @NCAJASPE FLOAT = 0,
            @NCAJASAS FLOAT = 0,
            @NPESO FLOAT = 0

    SELECT @NCAJASAS = SUM(B.QCAJASIGP + (B.QBOTASIGP / C.QCONTENIDO)),
           @NCAJASPE = SUM(B.QCAJPEDID + (B.QBOTPEDID / C.QCONTENIDO)),
           @NPESO = SUM(C.QPESO * ISNULL(B.QCAJASIGP + (B.QBOTASIGP / C.QCONTENIDO), 0))
    FROM #DATA_PEDIDOS A WITH (NOLOCK)
        INNER JOIN TPEDID2F B WITH (NOLOCK) ON A.COMPANIA = B.COMPANIA AND A.SUCURSAL = 
    B.SUCURSAL AND A.DOCUPEDIDO = B.DOCUPEDIDO AND A.NROPEDIDO = B.NROPEDIDO
        AND A.CLIENTE = B.CLIENTE
        INNER JOIN MARTIC1F C WITH (NOLOCK) ON A.COMPANIA = C.COMPANIA AND B.ARTICULO = 
    C.ARTICULO
        INNER JOIN MLINEA1F F WITH (NOLOCK) ON C.COMPANIA = F.COMPANIA AND C.LINEA = 
    F.LINEA AND F.FLGLINEA='Te'

    -- SETEAMOS VALORES DE BITACORA
    UPDATE TPLINT3F
    SET OPSENVIO = @OPSENVIO,
        NPEDIDEN = @NTOTAL,
        NCAJASPE = @NCAJASPE,
        NCAJASAS = @NCAJASAS,
        NPESO = @NPESO
    WHERE COMPANIA = @COMPANIA
        AND SUCURSAL = @SUCURSAL
        AND EMISOR = @EMISOR
        AND ID = @ID

END

```