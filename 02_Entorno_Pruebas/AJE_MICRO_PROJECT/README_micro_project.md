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

4. 

## Simulacion cadena de suministros/Avail/Items.docx
