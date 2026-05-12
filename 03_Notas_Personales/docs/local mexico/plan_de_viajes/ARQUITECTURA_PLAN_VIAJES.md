# Detalle de la documentacion
## Plan de viajes: centro de la integracion
El corazon  de la integracion es **Plan de viajes** pues contiene los archivos .wsdl , estos servicios SOAP fungen de contratos de la API, nos indican que datos enviar y que esperar.

[detalle de los wsdl y soap](../TECH_NOTES.md#Teoria-acerca-de-los-.wsdl-y-SOAP)

En Plan de viajes es donde la logistica fisica se convierte en datos digitales.De modo que si el plan de viajes falla , el producto no sale del almacen, las facturas no se generan y los camiones no se mueven. 

Contiene la mayor cantidad de archivos .wsdl , lo cual implica que es un **bus de servicios** . Habla con :
- Recursos humanos (WSEmpleados) 
- Finanzas (WSProcesoNomina)
- Estructura logistica (WSCiudad,WSArea)
- ERP (WSCompania)

Para que un camion AJE salga a la ruta , el sistema necesita validar los datos que vienen de todas partes
- Validacion de identidad: El empleado esta activo(WSEmpleados)
- Validacion geografica : La ruta es valida? (WSCiudad WSArea)
- Validacion Legal/Fiscal: la compañia esta habilitada para facturar ese viaje? (WSCompania)


Diagrama del actual plan de Viajes
<p align="center">
    <img src="../../imagenes/plan_viajes.png" width="80%">
</p>
como se ve,presenta una arquitectura hibrida, conecta el mundo web con los servidores corporativos.

### Componentes criticos
- Zona de usuario(izq): Vemos navegadores accediendo a URLs de Ajemex (como testsolicitudes.ajemex.net). Pasan por un WAF (Web application firewall) que es la primera capa de seguridad 

-  Zona de Aplicacion : Aqui vive la logica , **Azure AppServices** (Fronted) y un componente vital llamado  **Portal de Solicitudes Ajemex API**

AppService Fronted se encuentra en una zona de visibilidad hacia el WAF, su funcion es servir de interfaz de usuario, en una zona publica/usuario.


- Zona de datos y procesamiento : los servidores que procesan los datos **ETL(10.0.56.7)** Prepara los datos de empleados para el plan de viajes; **WS LINUX(10.0.56.4)** Es el servidor que probablemente aloja esos archivos **.wsdl** , estos serviores son nodos de computo.El ETL transforma los datos y WS linux ejecuta comandos SOAP.consumen datos de → y los entregan a ← . 

Mientras que AppService Interface Backend(Zona de datos/core) , aunque tecnicamente es un servicio de aplicacion , se situa dentro de Virtual Network interna.Esta en la zona de datos, porque actua como un proxy de integracion o GATEWAY que tiene permisos exclusivos para consultar las bases de datos y servicios SOAP , no sera accesible desde internet sino solo a traves del frontend.Como se ve el backend reside en el mismo segmento de red para minimizar la latencia y maximizar la seguridad.


- Zona de almacenamiento y directorio: 
**SQL SERVER(DMRRHHMXTEST)** y servidor AD (10.0.4.5) representan el backend de datos(System of Record) . Estan en un segmento de red distinto.
Esta separacion suele representar una DMZ interna o una subred de datos protegida. 

```bash
+----------------------+-----------------------+----------------------------------+
|      Componente      |   Zona en Diagrama    |         Función Técnica          |
+----------------------+-----------------------+----------------------------------+
| Frontend AppService  | Aplicación            | Interfaz de Usuario y Autentic.  |
+----------------------+-----------------------+----------------------------------+
| Backend AppService   | Datos                 | Gateway e integración interna    |
+----------------------+-----------------------+----------------------------------+
| ETL & WS Linux       | Procesamiento         | Lógica de negocio y SOAP         |
+----------------------+-----------------------+----------------------------------+
| SQL DMRRHHMXTEST     | Persistencia (Der.)   | Almacén central datos RRHH       |
+----------------------+-----------------------+----------------------------------+
| BD MAGIC (AWS)       | Nube Externa          | DB Maestra (Fuera de Azure)      |
+----------------------+-----------------------+----------------------------------+
```
Un breve resumen : 
nivel 1: acceso externo , navegadores y WAF, nivvel 2: zona de aplicacion, fronted y portal de solicitudes API, nivel 3: zona de datos y procesamiento , nodos de computo ETL y WSLINUX y el backend interface; nivel 4: zona de persistencia/core : SQL server , servidor AD y el salto a AWS (BD magic)


## Eje de datos: Cadena de suministros (Avail & EflextIA) 

### Avail

Gestion de maestros y produccion (MRP/WMS) los nombres de los archivos corresponden a objetos estandares de un sistema de planificacion de recursos. 
- **items.docx** y **boms.docx** definen los materiales y las recetasx de produccion. (materia prima para una bebida)

- **InvActs.docx** (Inventory Activities) Registra los movimientos de stock en tiempo real

- **ShipActs.docx**  y **ShipSchd.docx** (Shiping schedules), gestionan la programacion de despachos y salidas del almacen

- **MakeActs** y **MakeBySegments**, el sistema rastrea la fabricacion por etapas o segmentos de produccion.

### EflexIA (T1 y T2) 
La division en T1 y T2 es una convencion logistica estandar
- T1 (transporte primario) suele referirse al movimiento de grandes volumenes desde la planta de produccion a los centros de distribucion (CEDIS).  
El archivo **anuncios regulares** seria una programacion fija de viajes de larga distancia

- T2 (transporte secundario) Se refire a la ultima milla o distribucion capilar (del CEDIS al punto de venta) El documento de integracion T2 sugiere que aqui la complejidad aumenta por cantidad de puntos de venta

SP BM Relacionados: Indica el uso de Stored Procedure par conectar la logica Big Magic con el sistema de transporte

```bash
+--------------+--------------------------+---------------------------------+
|   Módulo     |    Enfoque Técnico       |       Entidades Clave           |
+--------------+--------------------------+---------------------------------+
| Avail        | Inventario y Manufactura | Items, BOMs, Producción (Make)  |
+--------------+--------------------------+---------------------------------+
| Efletex T1   | Logística Primaria       | Despacho Planta -> CEDIS        |
+--------------+--------------------------+---------------------------------+
| Efletex T2   | Logística Secundaria     | CEDIS -> Cliente Final          |
+--------------+--------------------------+---------------------------------+
| Integración  | ETL y Stored Procedures  | Sincronización Avail <-> BM     |
+--------------+--------------------------+---------------------------------+
```
El plan de viajes no es un ente aislado, es el consumidor final de la info generada en la cadena de suministros.
Existe una **dependencia de datos maestros** , el plan de viaje orquesta lo que avvail y efletex preparan

Para que el proceso en el diagrama de azure/aws se ejecute, requiere los insumos de la cadena de suministros. 

De avail se obtiene los items y los boms , qué se transporta y cómo se compone la carga respectivamente.Sin esto el plan de viaje no tiene contenido. De efletex (t1/t2) obtiene **las rutas y la disponibilidad** de transporte, plan de viajes es la ejecucion de un anuncia de transporte Efletex

Esto en un diagrama
```bash
[ CADENA DE SUMINISTRO ]                 [ INFRAESTRUCTURA PLAN DE VIAJES ]
(Fuentes de Datos)                       (Procesamiento y Ejecución)
          |                                          |
          v                                          v
+-----------------------+              +-----------------------------------+
| AVAIL (Manufactura)   |              | AZURE APP SERVICE (Frontend)      |
| - Items / BOMs        |----------+   | - Interfaz de Usuario             |
+-----------------------+          |   +-----------------------------------+
          |                        |                 |
          v                        |                 v
+-----------------------+          |   +-----------------------------------+
| EFLETEX (Transporte)  |          +-->| PORTAL SOLICITUDES API (Backend)  |
| - T1 / T2 Routes      |------------> | - Valida contra SQL / AD          |
+-----------------------+              +-----------------------------------+
          |                                          |
          v                                          v
+-----------------------+              +-----------------------------------+
| BIG MAGIC (AWS)       |<-------------| WS LINUX / SOAP SERVICES          |
| - Master Data Hub     |              | - Ejecuta el contrato de viaje    |
+-----------------------+              +-----------------------------------+
```
El punto de integracion en el diagrama plan-viajes
- El proceso ETL (10.0.56.7) no solo prepara los datos de empleados , sino que tambien importa los **ShipSchd** (programas de envia) de AVAIL para que aparezcan en el portal.


ETL(10.0.56.7) integra los datos de Avail en el plan de viajes, pues la analizar los documentos que detallan el mapeo de datos y la configuracion del flujo, se llega a esa conclusion.

**cadena de suministros/avail/conectivida y sincronizacion con AVAIL mediante ETL.docx** 

#### Big magic es el ERP central 
- confirmacion de datos logisticos : Log jobs del Glue detallan que BM envia a AVAIL los ITEMS, BOMS(receta) ,INVACTS(inventario) y SHIPSCHID(plan de distribucion)


**cadena de suministros /Avail/ShipSchd.docx**


- El stored procedure clave: para el cumplimiento del plan de distribucion (SHIPSCHID) se usa el SP **Av10_ILRB** , este trabaja la info antes de que el ETL la mueva.

**Transversal/Integrados BM/Documentacion tecnica integrados maestros.docx**

Eslabon entre la cadena de suministros y el portal de viajes
#### La conexion con el plan de viajes (proceso Intercompany)

- Proceso intercompany: el codigo SQL incluye , **PR_ERP_FNZ_QRY_GN_ObtenerOrdenCompraInterface**, es el encargado de cruzar la informacion entre compañias(ej Ajemex comprando a alpamayo)
- Este proceso permite visualizar guias TVC  y Facturas, que son la base legal y operativa de los viajes
- Uso de la API: El codigo muestra que el sistema consume una URL **http://10.101.60.228:8080/integrador-maestro/ejecutaFuncion** , esta es la misma PORTAL solicitudes Ajemex API que vimos en el diagrama central.

```bash
[ ERP BIG MAGIC ] --> [ ETL / AWS GLUE ] --> [ AVAIL / POSTGRES ]
      |                      |                      |
      | (Datos Maestros)     | (Jobs: SHIPSCHD)     | (Plan de Producción)
      v                      v                      v
[ SQL INTERMEDIA ] --> [ INTEGRADOR MAESTROS ] --> [ PORTAL PLAN VIAJES ]
(10.100.199.10)        (10.101.60.228)             (Azure AppService)
```

Resumen :
1. Avail es el receptor del plan de distribucion generado en big magic.
2. El etl 10.0.56.7 actua como puente que extrae los deltas de inventario y movimiento invact y shipschd para que el portal de viajes sepa quee mercania esta ista para ser transportada.
3. la seguridad se maneja mediante terminal services RDP y tokens bearer.Lo quee see explica por WAF AD etc 

**transversal/Extraccion ETL - Microsofft Fabrics/PROCESO DE EXTRACCION MICROSOFT FABRIC.docx**

En la lista de tablas Microsoft Fabric , aparecen las tablas maestras de recursos humanos de Big Magic:
- MPERSOEF, MPERSOGF, MPERSO7F, MPERSO1F, MPERSO8F, MPERSOCF, MPERSODF, todas estas tablas  contienen los datos maestros de personal empleados, cargos , sucursales asignados.

- El procesor de extraccion hacia Fabric (y el ETL) efectivamente prepara la base de empleados que luego consume el potal de viajes para saber quien esta solicitando la orden de gasto(OG) .

Fabric no solo consultas tablas de personal, sino tambien inventaros y logistica BARTIC TCOALM, esto sugiere que fabric se usa para auditoria y reporting del gasto que el portal genera

**Local Mexico/Plan de Viajes/InsertaOG.swdl**

Es la pieza final, confirma como el portal de viajes le devuelve la informacion a Big Magic.

- EndPoint : Se comunica con **https://10.0.56.4:8443/aje-auth-ad-ws-bm/services/InsertaOG** 10.0.56.4 esta en el mismo segmento que 10.0.56.7 , confirmando que esa zona de la red es la encargada de la comunicacion con el ERP.

- Operacion: InsertaOV2 , este servicio recibe **plan_viaje_id** y **solicitante** y el **total_plan_viaje** 

- Relacion con **ShipSchid** aunque el wsdl no menciona explicitamente "avail" , el campo objetivo o los metadatos del plan_viaje_id son los que vinculan la orden de gasto con el programa de envio ShipSchd, que etl importo previamente.

- DB MAGIC(AWS) , es el punto de union , EFLETEXTIA- (t1/t2) rutas y disponibilidades de transporte guarda aqui los procedimientos (SP BM relacionados) y el WS Linux

El portal de viajes no solo lee datos, cuando el viaje se aprueba , el azure appservice consume el wsdl en la ip **10.0.56.4** (big magic ws)

Los maestros no son solo nombres , incluyen la jerarquia completa de la compañia(BGEREN1F,BREGION1F,BCNFIN1) para que el portal sepa que nivel de aprobacion requiere cada viaje.

```bash
+---------------------------------------------------------------------------------+
|                          CORE ERP (AS400 / BIG MAGIC)                           |
|                                                                                 |
|       +-------------------+                     +------------------------+      |
|       |   ERP BIG MAGIC   | <------------------ |  Web Service (SOAP)    |      |
|       | (Tablas Maestras) |  (Crea Orden Gasto) |      10.0.56.4         |      |
|       +---------+---------+                     +-----------^------------+      |
+-----------------|-------------------------------------------|-------------------+
                  |                                           |
                  | (Extracción Tablas "F")                   | (Consumo WSDL)
                  v                                           |
+-------------------------------------------------------------|-------------------+
|                     CAPA DE DATOS Y ETL                     |                   |
|                                                             |                   |
|  +------------------+      +------------------+             |                   |
|  | MICROSOFT FABRIC |      |  SQL INTERMEDIA  |             |                   |
|  | (MPERSO, BARTIC) |      |  10.100.199.10   |             |                   |
|  +------------------+      +--------+---------+             |                   |
|                                     |                       |                   |
|  +------------------+               | (Sync Maestros)       |                   |
|  |  AWS GLUE / ETL  |               v                       |                   |
|  |    10.0.56.7     |      +------------------+             |                   |
|  | (Job: SHIPSCHD)  |      |    INTEGRADOR    |             |                   |
|  +---------+--------+      |    10.101.60.228 |             |                   |
+------------|---------------|--------+---------+-------------|-------------------+
             |               |        |                       |
             | (Plan Prod.)  |        |                       |
+------------v---------------|--------|-----------------------|-------------------+
|     OPERACIÓN LOGÍSTICA    |        |  FRONT-END Y LÓGICA   |                   |
|                            |        |                       |                   |
|    +------------------+    |        |    +------------------+--------+          |
|    | AVAIL / POSTGRES |----+        +--->|   PORTAL PLAN VIAJES      |          |
|    | (Ship Schedule)  |                  |    (Azure AppService)     |          |
|    +------------------+                  +---------------------------+          |
+---------------------------------------------------------------------------------+

```
Notas: 
- el cierre del ciclo: el flujo ahora es bidireccional, la informacion sale por la SQL intermedia pero regresa "procesada" como gasto financiero a traves de WEb Service (10.0.56.4)

- microsoft fabric: actua como espejo de auditoria, si el portal dice que se gastó $X en un viaje para el empleado Y , en fabric se debe cruzar esa OG (orden de gasto) con la tabla MPERSOE de personal para validar que el gasto es legitimo.

- Desacoplamiento , el integrador (10.101.60.228) sigue siendo el "traductor" que evita que el portal azure tenga que hablar directamente con el 


```bash
[ NUBE / AZURE ]                 [ ON-PREMISE / DATA CENTER ]
+--------------------------+          +------------------------------------+
|  PORTAL PLAN DE VIAJES   |          |    SERVIDOR INTEGRACIÓN (API)      |
|    (App Service)         | <------> |          10.101.60.228             |
+------------+-------------+          +-----------------+------------------+
             |                                          |
             | (Retorno OG via SOAP)                    | (Consulta Maestros)
             v                                          v
+--------------------------+          +------------------------------------+
|   WEB SERVICE GATEWAY    |          |       SISTEMA CENTRAL (CORE)       |
|      10.0.56.4           | <------> |            AS400 / IBM i           |
|  (Capa Axis2/Java)       |          |        [ ERP BIG MAGIC ]           |
+--------------------------+          +------------------------------------+
                                                ^              ^
                                                |              |
                                        (Tablas F)            (ETL Glue)
                                                |              |
                                      +---------+-------+   +--+-----------+
                                      | MICROSOFT FABRIC|   |  AVAIL / PG  |
                                      +-----------------+   +--------------+
```
Big magic es un ERP que corre tradicionalmente sobre AS400(IBM i) .

- La nomenclatura de las tablas el prefijo F mpersoef, mcliente8F, bartic3F , tienen que ver con el hecho de que AS400 / DB2 la F al final suele hacer referencia  a physical file. Ademas los sistemas legados desarrollados en RPG o cobol para as400 estructuran sus bases de datos de esa forma.


## La capa Transversal : Microsofft Fabric & RFID

Es la frontera final , no sirve tener una OG si el camion no ha pasado por el arco de lectura

- Ingresos de almacen , el RFID automatiza lo que antes se hacia en manual.
- La conexion, cuando el tag lee un pallet, dede disparar una actualizacion en las tablas de movimientos de almacen(TC0ALMIF)de la lista Fabric.

```bash
[ CAPA TRANSVERSAL / ANALÍTICA ]
                                +-----------------------------+
                                |      MICROSOFT FABRIC       |
                                | (Auditoría de Tablas "F")   |
                                +--------------^--------------+
                                               | (Sincronización)
+-----------------------+       +--------------+--------------+       +-----------------------+
|  CAPA FÍSICA (RFID)   |       |    CORE ERP (AS400)         |       |  LOGÍSTICA (AVAIL)    |
|                       |       |      BIG MAGIC              |       |                       |
| [Antenas en Almacén]  |------>|  (Tablas: BARTIC, TCOALM)   |<------|  [ETL AWS GLUE]       |
|  Lee Movimientos de   | (Sync)|  (Contabilidad y Maestro)   | (Items|  Sincroniza Planes    |
|  Inventario Físico    |       +--------------+--------------+  /BOM)|  de Producción        |
+-----------------------+                      |                      +-----------+-----------+
                                               |                                  |
      +----------------------------------------+-----------------------+          |
      |                                                                |          | (Data Feed)
      v                                                                v          v
+-----------------------+       +------------------------------+      +-----------------------+
|  WEB SERVICE (SOAP)   |       |  INTEGRADOR DE MAESTROS      |      |      EFLETEX IA       |
|      10.0.56.4        |       |      10.101.60.228           |      |                       |
|  (Inserta OG / Gasto) |<------+  (Traductor de Idiomas)      |<-----|  (Motor de Rutas e    |
+-----------^-----------+       +--------------+---------------+      |   Inteligencia)       |
            |                                  |                      +-----------+-----------+
            |                                  |                                  |
            |            +---------------------v-----------------------+          |
            |            |       PORTAL PLAN DE VIAJES (Azure)         |          |
            +------------|   (Donde el usuario crea la ruta y el       |<---------+
                         |    gasto basado en lo que dice EfletexIA)   |
                         +---------------------------------------------+
```

