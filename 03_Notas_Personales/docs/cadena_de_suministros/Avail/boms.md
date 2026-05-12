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
