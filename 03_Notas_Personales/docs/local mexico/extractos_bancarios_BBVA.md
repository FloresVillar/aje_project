### SECCIÓN: INTEGRACIÓN DE EXTRACTOS BANCARIOS BBVA

#### Proceso de registros de extractos

1. En el servidor **10.0.16.6** se encuentra alojado un apache tomcat con una aplicación que se ejecuta cada 5 min, la cual hace la lectura de los archivos de extractos bancarios y registra el contenido en una tabla temporal en la **MXBDAJE**.

* La aplicación java realiza un insert en las siguientes tablas:

```bash
INSERT INTO TMP_BCO_EECC(COMPANIA, LINEA, TEXTO, ARCHIVO, FECHA, FLGPROCESADO, USUARIO) VALUES(?,?,?,?,?,?,?)
INSERT INTO TMP_BCO_EECC_FIX(COMPANIA, LINEA, TEXTO, ARCHIVO, FECHA, FLGPROCESADO, USUARIO) VALUES(?,?,?,?,?,?,?)
```

* **Campos de la tabla TMP_BCO_EECC y TMP_BCO_EECC_FIX**
    * **COMPANIA**: Compañía
    * **LINEA**: Número del archivo
    * **TEXTO**: Texto de la línea en curso
    * **ARCHIVO**: Nombre del archivo procesado
    * **FECHA**: fecha
    * **FLGPROCESADO**: Admite valor 0 - No procesado, 1 - procesado
    * **USUARIO**: valor fijo SISINTBCO

**Ejemplo del contenido de un extracto bancario:**

```bash
11000000000120523062
220002114500083301638      PAGO CUENTA DE TERCERO  BNET   1509678998 Ajemex
00000000001000.000000002347014.03N06099805/03/2614:58:4505/03/2605/03/26
```

2. En la **MXBDAJE** se tiene el job: **MX33_REPLICAR_EECC_BANCOS**, este job se encarga de tomar los datos de los extractos bancarios de las tablas temporales **TMP_BCO_EECC**, el job en sus step tiene la ejecución del siguiente stored procedure:

* **USP_BCO_EECC_IMPORTAR_REPLICAR**: Este job no recibe ningún parámetro y se encarga de orquestar el registro de los extractos en la MXBDAJE.
* **Stored procedures relacionados:**
    * `USP_BCO_EECC_IMPORTAR_0002`
    * `USP_BCO_EECC_IMPORTAR_REPLICAR_FIX`
    * `USP_BCO_EECC_IMPORTAR_0002_FIX`

> **Nota:** Hay 2 tablas **TMP_BCO_EECC** y **TMP_BCO_EECC_FIX**, la **TMP_BCO_EECC** esta en un proceso automatizado, y la **TMP_BCO_EECC_FIX** y los stored procedure que terminan en FIX se agregaron para realizar una ejecución manual de todo el proceso.

#### Descripción Detallada del Flujo de Interfaz Bancaria

**1. Preparación de Insumos (Proceso Externo)**

*   **Paso 01:** La **Aplicación de Bancomer** inicia la descarga de los estados de cuenta o archivos de movimientos en formatos planos (`.txt`). Los archivos son depositados en una ruta específica del **Sistema de Archivos (Disco)**, actuando como la "bandeja de entrada" para el proceso de integración.

**2. Extracción y Carga (Java Tomcat - ETL)**

*   **Paso 02:** El **Job de Java Tomcat**, configurado mediante una tarea programada cada 5 minutos, escanea la carpeta de entrada en el Disco buscando archivos nuevos o recientes.
*   **Paso 03:** El Sistema de Archivos retorna el flujo de datos (stream) al servidor Tomcat para su procesamiento en memoria.
*   **Paso 04:** La aplicación Java parsea el contenido y realiza el **INSERT** de los registros en las tablas de la base de datos **MXBDAJE**. En este punto, los datos suelen estar en un estado "crudo" o temporal.

**3. Gestión de Archivos (Limpieza)**

*   **Paso 05:** Una vez que la base de datos confirma la recepción de los datos, el componente Java solicita al Disco mover el archivo original de la carpeta de entrada a la carpeta de **Procesados/**. Esto evita que el archivo se lea doblemente en el siguiente ciclo de 5 minutos.

**4. Procesamiento de Negocio (Base de Datos)**

*   **Paso 06:** El **Job de la Base de Datos** se dispara (ya sea por un evento de inserción o por un horario definido) para iniciar la transformación de los datos.
*   **Paso 07:** El **Stored Procedure** realiza la lectura de los registros recién insertados en las tablas de **MXBDAJE**. Se ejecuta la **Lógica de Negocio**: aquí se aplican validaciones de integridad, limpieza de duplicados y cruce de información bancaria.
*   **Paso 08:** El procedimiento realiza el **Registro Final en las Tablas de Movimientos** definitivas, quedando la información lista para ser consultada por el usuario final o sistemas contables.

#### Diagrama de Flujo del Proceso (Secuencia)

```bash
 App Bancomer      Sistema de Archivos      Java Tomcat (Job)      BD (MXBDAJE)      Job / SP

      |                     |                      |                    |                |
      | [ Proceso Externo ] |                      |                    |                |
  (1) | Descarga y guarda   |                      |                    |                |

      |---- archivos ------>|                      |                    |                |
      |    (.csv / .txt)    |                      |                    |                |
      |                     |                      |                    |                |
      |                     | [ Se activa cada 5 min ]                  |                |
      |                     |                      |                    |                |
      |                     | (2) Busca archivos   |                    |                |
      |                     |<---------------------|                    |                |
      |                     |                      |                    |                |
      |                     | (3) Retorna flujo    |                    |                |
      |                     |------- de datos ---->|                    |                |
      |                     |                      |                    |                |
      |                     |                      | (4) INSERT de      |                |
      |                     |                      |----- registros --->|                |
      |                     |                      |                    |                |
      |                     | (5) Mueve archivo    |                    |                |
      |                     |<--- a procesados ----|                    |                |
      |                     |                      |                    |                |
      |                     |                      |           [ Disparo por evento ]    |
      |                     |                      |                    |                |
      |                     |                      |                (6) | Lectura tablas |
      |                     |                      |                    |<---------------|
      |                     |                      |                    |                |
      |                     |                      |                (7) | Ejecuta Lógica |
      |                     |                      |                    |<---------------|
      |                     |                      |                    |  (Stored Proc) |
      |                     |                      |                    |                |
      |                     |                      |                (8) | Registro Final |
      |                     |                      |                    |<---------------|
      |                     |                      |                    |                |
```

[Fin del Documento de Extractos Bancarios BBVA]
