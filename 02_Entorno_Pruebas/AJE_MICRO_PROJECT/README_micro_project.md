## Emulacion del sistema big-magic , plan de viajes, portal de viajes, etc

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
## Emulacion de "Administracion de Personal" y "Gestion de nominas"

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
  [ Portal RRHH ] ──────┘          │      📂 [ mpersoef_2.csv ] ◀══ BIND MOUNT
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