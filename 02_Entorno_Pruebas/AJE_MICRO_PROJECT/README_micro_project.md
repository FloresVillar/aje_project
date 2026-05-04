## Simulacion del sistema big-magic , plan de viajes, portal de viajes, etc

1. Portal de viajes Envia la solicitud **solicitud_viaje** (un diccionario con claves viaje_id, empleado,total)al endpoint **http://integrador_api:8080/ejecutaFuncion** 

2. Integrador recibe el json desde **portal_viaje** , lo traduce a xml (SOAP) y envia **data=soap_xml** a **AS400**  al endpoint **http://as400_core:5001/services/InsertaOG**

3. En AS400 se agrega esa **data** que procede de integrador a **db_erp['ordenes_gasto']** y se  retorna el mensaje de exito en formato XML mediante SOAP(simulado)

4. De nuevo en integrador esa respuesta se encapsula dentro de un diccionario **{'status':..,'respuesta_soap':respuesta.text}**

5. Portal_viajes.py habia enviado la solicitud que inició el flujo en **respuesta = request.post(..,solicitud_viaje)** y se imprime la **respuesta**.

```bash
docker compose up --build


portal_viajes     | []PORTAL]Enviando solicitud a integrador...

portal_viajes     | respuesta final
portal_viajes     | {'respuesta_soap': '<soap:Envelope>             <soap:Body>Exito</soap:Body>             </soap:Envelope>', 'status': 'Proceso en ERP'}
fabric_monitor exited with code 0
portal_viajes exited with code 0
```
```bash
PORTAL VIAJES (JSON)          INTEGRADOR (Proxy/SOAP)           AS400 CORE (ERP)
   (Cloud/Azure)              (Middleware/WildFly)               (On-Premise)
 ───────────────────           ───────────────────            ───────────────────
          │                             │                              │
 (1) [POST] /ejecutaFuncion             │                              │
     {JSON Data} ──────────────────────▶│                              │
          │                             │                              │
          │                    (2) [Traducción]                        │
          │                        JSON ➔ XML                          │
          │                             │                              │
          │                             │ (2) [POST] /services/InsertaOG
          │                             │     <soap:Envelope> ────────▶│
          │                             │                              │
          │                             │                    (3) [Persistencia]
          │                             │                        db_erp['OG']
          │                             │                              │
          │                             │ (3) [Response] 200 OK        │
          │                             │     <soap:Body>Exito</... ◀──┘
          │                             │                              │
          │                    (4) [Encapsulamiento]                   │
          │                        XML ➔ Dict                          │
          │                             │                              │
 (5) [Response] 200 OK                  │                              │
     {status:..., soap:...} ◀───────────┘                              │
          │                             │                              │
   [Imprime Respuesta]                  │                              │
          ▼                             │                              │
```
## Simulacion full-Step

1. FullStep Saas inicia el proceso enviando el diccionario **adjudicacion_compra** con el metodo **registrarAdjudicacion** y los datos de orden/proveedor , al endpoint del integrador en **http://wildfly_integrador_api:8080/ejecutaFuncion**
2. Integrador recibe el JSON, identifica que no es un viaje (else) y mapea el **metodo_wsdl** para construir el **soap_xml** que necesita el core legacy
3. Integrador despacha la peticion POST con el xml al endpoint de red del core **http://as400_core:5001/services/ComprasAjeGroupWSBinding**
4. AS400 (capa de red) recibe el xml en la funcion **compras_binding** extrae los parametros y deleg la ejecucion a la **capa de datos** invocando a **sp_registrar_compra_aje**
5. AS400 (capa de datos) ejecuta la logica interna del Stored Procedured, imprime el log "logica interna" y persiste la informacion en la lista **db_erp["compras_fullstep]"** 
6. AS400 retorna un sobre SOAP XML con el mensaje de "estilo fullstep" hacia el integrador
7. Integrador recibe la respuesta del Core, la encapsula en un JSON con la clave **respuesta_soap** y finaliza la peticion HTTP iniciada por fullstep
8. FullStep recibe el objeto de respuestaa y lo imprime en consola para confirmar que la adjudicacion fue procesada correctamente en el ERP


```bash
SISTEMA EXTERNO (SaaS)          MIDDLEWARE (WS LINUX)                CORE ERP (AWS CLOUD)
   [FullStep SaaS]            [WildFly Integrador]                [SRVGLZADB01 / BM]
-----------------------      ----------------------          -----------------------------
          |                             |                               |
          |  1. POST (JSON)             |                               |
          |---------------------------->|                               |
          |  (adjudicacion_compra)      |                               |
          |                             |                               |
          |                             |  2. Traduce JSON a XML/SOAP   |
          |                             |  3. POST (SOAP XML)           |
          |                             |------------------------------>|
          |                             |  (registrarAdjudicacion)      |
          |                             |                               |
          |                             |                               |  4. Capa de Red (WSDL)
          |                             |                               |     recibe XML
          |                             |                               |           |
          |                             |                               |  5. Capa de Datos (SP)
          |                             |                               |     sp_registrar_compra_aje
          |                             |                               |           |
          |                             |                               |  6. Persistencia Física
          |                             |                               |     db_erp['compras_fullstep']
          |                             |                               |           |
          |                             |  7. HTTP 200 (SOAP XML)       |           |
          |                             |<------------------------------|-----------'
          |                             |    (Exito FullStep)           |
          |                             |                               |
          |  8. Respuesta (JSON)        |                               |
          |<----------------------------|                               |
          |  (respuesta_soap)           |                               |
          |                             |                               |
```
```bash
+-------------------------+-----------------------------------+---------------------------------------------------------+
|  COMPONENTE EN CÓDIGO   |    EQUIVALENCIA EN SISTEMA AJE    |                    ROL / FUNCIÓN                        |
+-------------------------+-----------------------------------+---------------------------------------------------------+
| fullsteps_saas          | FullStep SaaS                     | Plataforma externa (SaaS) de licitaciones y compras.    |
+-------------------------+-----------------------------------+---------------------------------------------------------+
| wildfly_integrador_api  | Servidor WS Linux (10.0.56.4)     | Middleware/Gateway: traduce JSON a SOAP (XML).          |
+-------------------------+-----------------------------------+---------------------------------------------------------+
| as400_core              | SRVGLZADB01 (10.101.14.184)       | Servidor de Base de Datos "Big Magic" (AWS Ohio).       |
+-------------------------+-----------------------------------+---------------------------------------------------------+
| registrarAdjudicacion   | WSDL Binding                      | Contrato de servicio en "ComprasAjeGroupWSBinding".     |
+-------------------------+-----------------------------------+---------------------------------------------------------+
| sp_registrar_compra_aje | Stored Procedure (SP)             | Lógica de negocio SQL (Capa de Datos Salesforce/Efletex)|
+-------------------------+-----------------------------------+---------------------------------------------------------+
| db_erp['compras_fstep'] | Tablas de Compra (F)              | Persistencia física de las Órdenes de Compra (OC).      |
+-------------------------+-----------------------------------+---------------------------------------------------------+
| database/               | S3 Bucket / EFS / Staging         | Zona de aterrizaje (Landing Zone) para archivos planos. |
+-------------------------+-----------------------------------+---------------------------------------------------------+
```

## Simulacion de "Administracion de Personal" y "Gestion de nominas"

Para esta emulacion suceden algunos problemas de ejecucion, mientras que pra la emulacion del sistema Big Magic los contenedores y los servicios en ellos no presentan mayor contratiempo.

Se añade **cloud_azure/portal_rrhh.py** y **sap_mx/procesar_nomina.py** , ademas modificamos **middleware_onprem/integrador_api.py**.

Al ejecutar **docker composer up --build** ,se presentan exit code = 1. Los logs me son de igual modo interesantes, los cuales se leen de **abajo** hacia **arriba**,veámoslos:
- **requests.exception.ConnectionError: ...(Caused by Neewconnectionerror("..Connection refused"))**. No se puedo conectar, **integrador_api** rechazó a **portal_viajes**

Esto pese a que en el up anterior portal_viajes no tenia ningun problema... FALTA DOCUMENTAR 
...
 
1. **Portal_rrhh/portal_rrhh.py** llama a /bmp/evento_activacion , se envia un payload con toda la informacion, via **request.post(url,json=payload)**
2.En **integrador_api.py** no se escribe directamente en la tabla, se llama a **http://as400_core:5001/services/ActualizaPersonal** mediante responde = requests.post(url,json=data) .Siempre escuhando todas las interfaces.

3. El **as400_core** actualiza **./database/mpersoef_2.csv** y se retorna un mensaje de confirmacion con codigo de salida 200.

4. De nuevo en integrador **respose.text** es devuelve dentro de un jsonify .

5. Esta es la respuesta que retorna a **portal_rrhh.py**

```bash
gestion_nomina    | 
gestion_nomina    |  [BPMN] ejecutand captura novedades..
gestion_nomina    | calculo y liquidacion 6 registros        
gestion_nomina    | [BPMN] evento fin: pago realizado, total:
```

```bash
ZONA CLOUD (Azure)          │          ZONA ON-PREMISE (Local)
    ───────────────────────────────┼──────────────────────────────────────────
                                   │
  [ Portal Viajes ] ────┐          │          [ AS400 Core ]
       (Python)         │          │         (Flask Legacy)
                        │          │                ║
                        ▼          │                ║ (Escritura Física)
                 [ Integrador ] ───┼───────────────▶║
                 (API Gateway)     │                ║
                        ▲          │                ▼
  [ Portal RRHH ] ──────┘          │       [ mpersoef_2.csv ] ◀══ BIND MOUNT
       (Python)                    │          (Recurso Compartido)
                                   │                ║
    ───────────────────────────────┼────────────────║──────────────────────────
                                   │                ║
       ZONA TRANSVERSAL            │                ║ (Lectura de Datos)
    ───────────────────────────────┼────────        ║
                                   │       │        ╠════════════════╗
                                   │       ▼        ▼                ▼
                                   │   [ Fabric Monitor ]   [ Gestión Nómina ]
                                   │      (Analytics)          (BPMN Process)
                                   │           │                     │
    ───────────────────────────────┼───────────┼─────────────────────┼─────────
                                   │           └──────────┬──────────┘
           RECURSO COMPARTIDO      │                      ▼
             DE VISUALIZACIÓN      │              [ Terminal Docker ]
                                   │               (Standard Output)
```

## simulacion de AWS Glue /AVAIL bombs

Simulamos procesos de negocio especificos.
1. Extraccion de maestros(Big Magic → Glue) Cuando llamamos a **GetBoms** se simula la ejecucion del Store Procedure **AV10_IBOMI**, en el proyecto este procedimiento "barre" las tablas del ERP Big Magic para extraer la recetas Tecnicas BOMs. En la simulacion el **as400_core** entrega el CSV de recetas , actuando como el servidor legacy de la planta.

2. El middleware de transformacion (El servidor SQL) : El servidor **SRVGAPCT58** normaliza esquemas, en la simulacion **integrador_api** toma esos datos y, antes de guardarlos, limpia campos o valida que el UserPer sea un numero decimal valido.

3. Sincronizacion mediante ETL (AWS GLue)
El hilo que se dispara represetna al Job de Glue  **ETLBomsJob-Corp**, en el proyecto es un proceso "Batch" que corre de forma automatica. El sistema se configura para que la nube lo procese periodicamente. En la simulacion el script se llama a si mismo , simulando la autonomia dde la nube AWS.

4. Actualizacion del plan de suministros(AVAIL) El destino final **avail_south_boms.csv** presenta la base de datos RDS Postgres **A10_SOUTH**. En el proyecto cuando los datos llegan a postgres, AVAIL los procesa para calcular cuanto material comprar.En la simulacion  **fabric_monitor** cumple esa misma funcion.Si se cambia un dato en el origen, el monitor avisara de la nueva receta , simulando como un planificador de suministros veria la actualizacion en su tablero de control.

Resumen:
- **as400_core** es el ERP Big Magic (legacy)
- **integrador_api** es el nexo AWS Glue ++ SQL de tranformacion
- **Fabric_monitor** Es el sistema AVAIL (Cloud Planning)

```bash
NIVEL DE ORQUESTACIÓN Y ETL (Simulación AJE)
      ──────────────────────────────────────────────

      [ CONTENEDOR: as400_core ]          [ CONTENEDOR: integrador_api ]
      ──────────────────────────          ──────────────────────────────
                  │                                     │
    (A) TABLA MAESTRA (BOMs)                            │  (B) HILO "ORQUESTADOR"
        [ iboms.csv ]                                   │      (Loop cada 120s)
                  │                                     │          │
                  │          (1) GET /GetBOMs           │◀─────────┘
                  │ ◀───────────────────────────────────│
                  │                                     │  (2) TRANSFORMACIÓN
                  │          (3) JSON Data              │      (Lógica Python)
                  │ ───────────────────────────────────▶│
                                                        │
      [ VOLUMEN COMPARTIDO ]                            │  (4) CARGA (LOAD)
      ──────────────────────                            │      (Escritura CSV)
                  │                                     │
        [ avail_south_boms.csv ] ◀──────────────────────┘
                  │
                  ▼
      [ CONTENEDOR: fabric_monitor ]
      ──────────────────────────────
      (5) CONSUMO (Analítica)
          "Vigilante de AVAIL"
```

## simulacion Invacts (aun no implementado en codigo)

1. **integrador_api** invoca a requests.post("http://127.0.0.1:8080/aws_glue/ETLInvAcstJob-Corp"), este jobs aparece en la lists de integraciones como el encargado de sincronizar el stock de PT(producto terminado) y MP(materia prima).

2. **Extraccion desde el ERP (Store Procedure AV10_ISIS)**
El integrador llama a http://as400_core:5001/services/GetInventory. 
En as400_core.py  este endpoint simula los Sps **AV10_ISIS_FLOOR** y **AV10_ISIS_RM**. Lee el archivo **database/invacts.csv** , que contiene los campos obligatorios LocCd (plnata) ItemCd (producto)  , InvQty (cantidad) AsOfStamp (fecha/Hora)

3. **Transformacion y mapeo(carga intermedia SRVGAPCT58)** El integrador recibe el JSON de inventario.Aqui se realiza la logica de negocio

    - convierte las unidades a "base UOM"(Unidad de Medida Base)
    - Valida que la fecha **InvTm** tenga el formato ISO correcto
    - Prepara el paquete para la tabla de interfaz **IINVACTS**

```bash
[ ERP AV10_ISIS ] (Legacy AS400)
               |
               | (1) GET /services/GetInventory
               v
    +-----------------------+
    |    INTEGRADOR API     | <--- (2) Recibe JSON/XML
    +-----------------------+
               |
               | (3) Invoca AWS Glue Job
               v
    +-----------------------+
    |     AWS GLUE ETL      | <--- (4) Procesa y Transforma
    +-----------------------+
               |
               | (5) Escribe CSV
               v
    +-----------------------+
    |   ./database/         |
    |  invacts.csv (Data)   | <--- (6) ¡Aquí vive el stock!
    |  items.csv   (Maestro)|
    +-----------------------+
               |
               | (7) Bucle while True (Lectura)
               v
    +-----------------------+
    |    FABRIC MONITOR     |
    +-----------------------+
    |   ¿ItemCd es STR?     |
    |   SI: "BIG COLA 3L"   | <--- (8) LOG FINAL EXITOSO
    |   NO: "Desconocido"   |
    +-----------------------+
```


## Simulacion cadena de suministros/Avail/Items.docx

Se representa la integracion completa del catalogo de maestros , de modo que los datos tecnicos de items den sentido a los invetarios y recetas del ecosistema.
1. **origen : AS400** Este modulo actua como el satelite **SRVGLZADB01** exponiendo la tabla de interfaz IITEMS
    - Generacion de datos: provee los atributos  maestros detallados en la documentacion como **ItemCd** o **ItemNm** (ej BIG COLA 3L ) y los flags de negocio **IsProd** e **isMatl**
    - calculos logisticos: Incluye el **BaseWt** (peso por unidad) y **ShipWt** (peso por pallet) fundamentales para simular la capacidad de carga de los camiones
    - Servicio : expone el endpoint **http://as400_core:5001/services/GetItems** para que los demas modulos consuman la informacion
2. **sincronizacion : integrador API(integrador_api.py)** Simula la funcion de AWS GLue mediante mediante el Job ETLItemsJob-Corp
    - Extraccion: Realiza una peticion POST al AS400 para obtener el JSOn maestro
    - Persistencia: Transforma los datos y los guarda fisicamente en **databases/items.csv** dentro del volumen compartido
    - Orquestacion: Este paso es el "disparador" que permite que el monitor pase de mostrar codigos numericos a nombres reales de productos
3. **Monitor inteligente: Fabric Monitor (fabric_monitor.py)** Actua como el motor AVAIl , realizando el cruce de dats JOIN en tiempo real
    - Auditoria de recetas: cruza el archivo de BOMS con el de Items para traducir codigos como **501068** a nombres descriptivos como **BIG COLA 3L**
    - Auditoria logistica: Utiliza el **BaseUoM** (ej CASE) para identificar la unidad de medida y multiplicar el stock actual (**InvQty**) por el **BaseWt** para informar el peso total de kg presentes en la planta
    - Deteccion de cambios: Gracias a los bind mounts cualquier cambio en el catalogo se detecta en desarrollo




```bash
USUARIO / FRONTEND
              |
      [ 1. Dispara Job ETL ]
              |
              v
      +-----------------------+
      |    INTEGRADOR API     | <--- (Simula AWS Glue / ETLItemsJob-Corp)
      |   (Puerto 8080)       |
      +----------+------------+
                 |
        [ 2. Petición GET ]
        [  /services/GetItems ]
                 |
                 v
      +-----------------------+      +--------------------------+
      |      AS400 CORE       |      |     DATABASE SHARED      |
      |   (Puerto 5001)       |      |    (Volumen /database)   |
      +----------+------------+      +------------+-------------+
                 |                                ^
        [ 3. Retorna JSON ]                       |
        [ Maestro de Items]                       |
                 |                                |
                 +-------[ 4. Escribe CSV ]-------+
                         [ items.csv / invacts.csv]
                                                  |
                                                  |
                         +------------------------+
                         |
                [ 5. Lee CSV y cruza datos ]
                         |
                         v
              +-----------------------+
              |    FABRIC MONITOR     | <--- (Simula Motor AVAIL)
              |    (Bucle Infinito)   |
              +----------+------------+
                         |
                [ 6. Salida en Logs ]
                [ "BIG COLA 3L: 140kg"]
```