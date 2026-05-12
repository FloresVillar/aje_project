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