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

### En la simulacion
#### El mapa de credenciales (seguridad y conectividad) 
Existen 3 nodos criticos por los que se enrutaran los datos.Se ha de configurar el contenedor **integrador_api** con variables de entorno:
- **origen(Big Magic)**: **SEVGLZADB01** en el puerto 54241
- Intermedia(SQL transformacion) : IP 10.100.199.0 puerto 1433, aqui vive la tabl IBOMS
- Destino(CLoud): Una instancia de RDS Postgres en AWS (**rds-postgresql-avail-latam.sur...**)

#### El catalogo de Jobs de AWS Glue

Ahora sabemos que no solo movemos recetas (BOMS). Las capturas muestran una suite completa de procesos ETL que podrian emular:
- **ETLtems-job-Corp**: Mueve articulos de producto terminado (PT) y Materia Prima (MP)
- **ETLInvAcstJob-Corp** Sincroniza inventarios
- **ETLMakeAcstJob-Corp** cumplimiento del plan de produccion.
- **ETLBomsJob-Corp** Recetas

#### La logica Bidireccional(AVAIL-BM) 
Un detalle crucial es que el flujo no es solo Big Magic hacia AVAIL , existen procesos de retorno.
- **ETLMakeSegmentJob-Corp** Envia el plan de produccion generado en AVAIL de vuelta a Big Magic
- **ETLShipSchdJob-Corp** Envia el plan de distribucion

#### Modificaciones de los scripts
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



    
