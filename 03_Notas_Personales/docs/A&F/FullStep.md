
## FullStep

Arquitectura

Este diagrama describe la arquitectura de integración entre la plataforma **Fullstep** y el entorno de **AWS Cloud**, conectando los servicios web con las bases de datos regionales.

---

### Esquema de Arquitectura (ASCII)

```text
  [ SAAS ]                   [ AWS CLOUD / East-2 ]
+----------+          +----------------------------------------------------+

|          |          |  [ VPC - 10.101.60.0/22 ]                          |
|          |          |  +----------------------------------------------+  |
|          |  Web     |  |  [ Private Subnet ]                          |  |
| Fullstep | Services |  |  +-------------------------+                 |  |
|          | <------> |  |  | GLOBAL-APP-WS-FULLSTEP |                 |  |
|          |          |  |  | PROD-ZA (10.101.60.68) |                 |  |
|          |          |  |  |                         |    [ AWS BM ]   |  |
+----------+          |  |  |        WildFly        --+--> (Bases de    |  |

                      |  |  |                         |     Datos)      |  |
                      |  |  +-------------------------+          |       |  |
                      |  +---------------------------------------|------+  |
                      +------------------------------------------|---------+

                                                                 |
            +--------------------+-------------------+-----------+-------+--------------------+
            |                    |                   |                   |                    |
     +------------+       +------------+      +------------+      +------------+       +------------+

     | BD MX      |       | BD Bolivia |      | BD CAM NTE |      | BD Perú (C)|       | BD CAM SUR |
     | 10.101.8.184|      | 10.101.10.167|    | 10.101.6.238|     | 10.101.10.143|     | 10.101.8.155|
     +------------+       +------------+      +------------+      +------------+       +------------+
```

---

### Detalle de Componentes y Direccionamiento

#### Infraestructura Core
*   **SaaS:** Fullstep (Web Services ComprasAjeGroup).
*   **Cloud Provider:** AWS Region East-2.
*   **Middleware:** Servidor **WildFly** en instancia `GLOBAL-APP-WS-FULLSTEP-PROD-ZA` con IP `10.101.60.68`.

#### Capa de Datos (AWS BM)
El servidor WildFly actúa como puente hacia las siguientes bases de datos regionales:


| País / Región | Base de Datos | Dirección IP |
| :--- | :--- | :--- |
| **México** | BD MX | `10.101.8.184` |
| **Bolivia** | BD Bolivia | `10.101.10.167` |
| **CAM Norte** | BD CAM NORTE | `10.101.6.238` |
| **Perú (C)** | BD Perú (C) | `10.101.10.143` |
| **CAM Sur** | BD CAM SUR | `10.101.8.155` |
| **Ecuador** | BD ECU/VE/CORP | `10.101.10.187` |
| **Perú (P)** | BD Perú (P) | `10.101.10.204` |

# Métodos ComprasAJE - FullSteppv3

## Definición del WSDL (SoapUI)


| Campo | Valor |
| :--- | :--- |
| **WSDL URL** | `http://10.101.56` |
| **Namespace** | `http://ajegroup.com` |
| **Binding** | `ComprasAjeGroupWSPortBinding` |
| **SOAP Version** | SOAP 1.1 |
| **Style** | Document |

---

## Lista de Métodos por Categoría

### 1. Anulación o Baja
*   `anularDocumentoCompra`
*   `cancelarOrden`
*   `CancelarRequerimiento`

### 2. Consulta
*   `ConsultarProveedor`
*   `listarMejoraActivoFijo`
*   `ListarPartidasPresupuestos`
*   `ListarTipoDeCambio`
*   `ListarTrabajosEnCurso`

### 3. Inserción
*   `registrarAdjudicacion`
*   `registrarOrdenCompra`
*   `registrarProveedor`
*   `registrarRequerimiento`





Es la "pieza hermana" del plan de viajes , pero enfocada a Compras y abastecimiento. Aqui se ve como se integra la plataforma externa FullStep (Saas de e-procurement) con el ecosistema de AJE.

<p align="center">
    <img src="../../imagenes/full_step.png" width="85%">
</p>

#### FullStep como SaaS

Está al lado izquierdo ,aparece como SaaS , es la plataforma donde los compradores de AJE gestionan las licitaciones , cotizaciones y seleccion de proveedores, esto es el ciclo de vida completa del abastecimiento.
- Negociaciones y adjudicacion: El metodo **INT 10 - Metodo resgistrarAdjudicacion** confirma que FullStep se encarga de la seleccion final del proveedor tras una licitacion.
- Gestion de proveedores: Existen metodos especificos como **INT 02 - Metodo Registrar Proveeddor** e **INT 03 - Metodo ConsultarProveedorHabilitado**.Esto indica que fullstep es el filtro que decide qué proveedores están aptos para trabajar con AJE antes de enviar la informacion al ERP.

- Solicitudes y pedidos: se gestionan desde el mantenimineto de articulos (INT 01) hasta la cancelacion de ordenes (INT13) cubriendo el flujo operativo.

### El servidor Wildfly (GLOBAL-APP-WS-FULLSTEP)

FullStep se comunica via **Web Services** con un servidor **WildFly** (un servidor de aplicacion Java) que está en la nube de AWS de AJE.
- Se identifica como **PROD-ZA | 10.101.60.65**.Esta ubicado en una Subred Privada dentro de VPC de Aws, lo que  garantiza que, aunque se comunique con saas externo (fullStep) , la logica de negocio y el acceso a las bases de datos ocurren en un entorno protegido.

- Rol de traductor y validador: Wildlfly no solo distribuye datos, ejecuta STORED PROCEDURED especificos en las bases de datos Big Magic, cada metodo SOAP es un procedimiento almacenado(PR_ERP_COM_QRY_GN....)
    - Ejemplo: cuando FullStep envia una adjudicacion ,Wildlfy dispara **PR_ERP_COM_QRY_GN_registrarAdjudicarOrdenCompra**

#### Compras Metodos SOAP ComprasAJE-fullSetpv3

**Naturaleza de la interaccion**<br> 
Es una integracion "a demanda" . No es un proceso por lotes(batch) que corre una vez al dia; cada vez que un comprador realiza una accion en FullStep , se dispara un mensaje XML.<br>
**Protocolo robusto**<br>
Se observa el uso de **soapenv:Envelope** y definiciones de esquema **xsi:schemaLocation**.Esto es critico porque el intercambio de ordenes de compra y adjudicaciones requiere una estructura rigida para evitar errores financieros.<br>
**Separacion de ambientes**<br>
La tabla detalla que existen EnddPoints distintos para **TEST** y **PROD** , lo que confirma un ciclo de desarrollo profesional para estas integraciones.

Es claro que qui ocurre la integración,los metodos se dividen en 3 funciones que impactan al ERP:
- Anulacion o baja: **cancelarOrden** o **anularDocumentoCompra**

- Consulta: métodos **consultarProveedor** o **listarPartidasPresupuestarias** , el sistema de compras preguntan al ERP ¿tenemos dinero en esta cuenta? ¿este proveedor existe?

- Insercion: **registrarOrdenCompra** y **registrarAdjudicacion** cuando fullstep termina un proceso de compra, empuja la orden de compra terminada hacia el ecosistema de AJE para que se convierta en un compromiso financiero.

#### Destino de los datos : AWS BM (base de datos)

A la derecha del diagrama de AWS se ve el bloque AWS BM con multiples bases de datos por el pais:
- BD MX (10.101.6.184) Mexico
- BD PERU (10.101.10.143) Peru
Todas las bases de datos son SQL SERVER en el bloque AWS BM

Lo destacable es que el servidor **WildFly** actúa como un **Hub**. Recibe la informacion de FullStep y, segun el pais que este comprando, distribuye la informacion a la base de datos del ERP Big Magic.

Como se conecta esto con el **Plan de viajes**  :
- validacion: asi como el plan de viajes valida empleados, aqui se validan proveedores y presupuestos

- Cierre contable: el plan de viajes genera una OG , este sistema genera una OC , ambas se registran en el mismo core (Big Magic)

- Arquitectura hibrida: Ambos usan SOAP(xml) para comunicar nubes externas(Azure en compras,fullstep en compras) con la red privada de AJE (10.x.x.x).

Resumiendo :
1. En **FullStep** se crea un requirimiento , se licita y se adjudica (INT 10) 
2. En **WidFly(10.101.60.65)** : Recibe el XMl de FullStep , valida el presupuesto en la BD del pais correspondiente (INT 07 - ListarPartidasPresupuestales) y registra la orden.
3. En big magic: Se ejecuta el Stored Procedure para asentar la orden de compra (OC), lo que permite que el almacen (AVAIL) este listo para recibir la mercancia.

<p align="center">
    <img src="../../imagenes/aws_bm.png" >
</p>

El siguiente diagrama es aun mas clarificador, pues indica como se comunica con plan de viajes
```bash
[ CAPA EXTERNA / SAAS ]             [ CAPA DE INTEGRACIÓN (AWS) ]
+-----------------------+           +------------------------------+
|       FULLSTEP        |           |       SERVIDOR WILDFLY       |
|  (Portal de Compras)  | <-------> |       (Hub de Servicios)     |
|   Licitaciones y OC   |   (SOAP)  |       (10.101.X.X)           |
+-----------------------+           +--------------+---------------+
                                                   |
                                                   | (Ruteo por País)
      +--------------------------------------------+
      |                |               |                |
      v                v               v                v
[ BD MÉXICO ]    [ BD PERÚ ]     [ BD ECUADOR ]   [ OTRAS SEDES ]
(10.101.6.184)   (10.101.10.143)  (10.101.X.X)     (Big Magic)
      |                |               |                |
      +----------------+-------+-------+----------------+
                               |
                               v
               +-------------------------------+
               |    CORE ERP (AS400 / BM)      |
               |  (Registro de Orden Compra)   |
               +---------------+---------------+
                               |
         +---------------------+---------------------+
         |                                           |
         v                                           v
[ OPERACIÓN LOGÍSTICA ]                     [ PLAN DE VIAJES ]
(Avail / EfletexIA)                         (Gasto de Viaje)
- Recibe lo comprado                        - Gestiona el traslado
- Genera ShipSchd                           - Genera la OG final
```
Resumiendo : 
- Widfly  es el director, a diferencia del integrador de maestros ( que es para consulta personal) el servidor wildfly en este diagrama se encarga de recibir las facturas y ordenes de compra de FullStep y enviarlas a la base de datos correcta.

- El origen del gasto: aqui nace la orden de compra,documento que señala **"le compramos esto a tal proveedor"**. Sin esta OC, el almacen (AVAIL) no sabría que recibir y el plan de viajes no tendria sentido (porque no habría mercancia que mover)

- Segmentacion por IP: ver que las bases de dato Mexico (**10.101.6.184**) y Peru (**10.101.10.143**) estan en la misma red **10.101.x.x** que el integrador de Maestros **10.101.60.228**.Esto confirma que toda la capa de "integracion y aplicacion" vive en el mismo segmento de red.

Los metodos SOAP que se ddetallan en el pdf **integracion Proceso Compras.pdf** , Widfly mira en el Big Magic si hay presupuesto , Wildfly inserta la adjudicacion en Big Magic y si la compra se cancela en FullStep , se libera el compromiso en el ERP.

**consulta** → **registro** → **anulación**

### Detalles de 20260309 - Py Lego MX - FullStep Compras

1. Articulos(INT 01)
    - Proceso: sincronizacion de catalogos de articulos
    - Accion: insercion y actualizacion de articulos
    - Logica: Usa el SP **PR_ERP_COM_QRY_RegistrarArticulos** para procesar datos tecnicos como codigos de integracion , familia de productos y unidades de medida
2. Registro de proveedores(INT 02)
    - Proceso: Alya y modificacion de proveedores en el ERP
    - Accion:  Los datos viajan del FullStep hacia el BigMagic
    - Logica: Valida informacion fiscal (RUC), correos electronicos y zonas postales a traves del SP **PR_ERP_COM_QRY_RegistrarProveedores**
3. Consulta de Proveedores (INT 03)
    - Proceso: Verificacion de habilitacion de proveedores para transacciones
    - Metodo: Consulta sincrona mediante Web Service usando **PR_ERP_COM_QRY_GN_ConsultarProveedorHabilitado**

4. Registrar requerimiento(INT 04)
    - proceso: creacion de solicitudes de compra regularizadas
    - componentes: manejo de cabecera de solicitud, detalles de articulos (cantidad, precio unitario, centro de costo) y niveles de aprobacion por usuario
    - persistencia : Ejecuta el **SP_ERP_COM_QRY_GN_RegistrarReqCompras** en el core
5. Cancelar Requerimiento (INT 05)
    - Proceso: Anulacion de solicitudes previamente enviada
    - Identificacion: Requiere el codigo de integracion y el numero de solicitud para procesar la baja mediante **PR_ERP_COM_QRY_GN_CancelarReqCompras**

6. Consultar Mejora Activo Fijo (INT 06)
    - Proposito: verificar si un gasto esta asociado a la mejora de un activo fijo inexistente.
    - Componente Core: invocacion al SP **SP_ERP_COM_QRY_GN_ConsultarMejoraAF**
    - Entrada clave: Requiere compañia y codigo del activo
7. Consultar Partidas Presupuestarias (INT 07)
    - Proposito: Validar la disponibilidad de presupuesto por centro de costos y partida antes de proceder con la compra.
    - Componente: **PR_ERP_COM_QRY_GN_ConsultarPartidasPresupuestarias**
    - Detalle: Centro de costo, Partida,Ejercicio y monto solicitado
8. Consultar trabajo en curso
    - Proposito: Consulta de proyectos u obras en ejecucion que requieren suministros
    - Componente core: SP **PR_ERP_COM_QRY_GN_ConsultarTrabajoEnCurso**
9. Consultar tipo de cambio
    - Proposito: Obtener la tasa de cambio oficial registrada en el ERP para la converison 
    - Componente Core: SP **PR_ERP_COM_QRY_GN_CosnsultarTipoDeCambio**
10. Integracion de Negociacion (INT 10)
    - Proposito: Es el paso critio donde se confirma el proveedor ganador y se formaliza la compra
    - Accion: Realiza un Insert en las tablas de Big Magic mediante **PR_ERP_COM_QRY_RegistrarAdjudicacionOrdenCompra**
    - Payload Critico:
        - Compania, Sucursal, Proveedor
        - ItemProceso (ej 2025/SVC/108991/1)
        - Moneda (ej MXN) y condicionPago
        - Detalles: Articulo, Precio , Cantidad y Aprobacion
Endpoint: 
**[http://10.101.](http://10.101.)x.x:8095/ComprasAjeGroupWS/Services/ComprasAjeGroupSOAPService?wsdl.** 
Frecuencia: Operan a DEMANDA , disparandose cada vez que un omprador o el sistema FullStep requiere validar datos o confirmar una adjudicacion.

11. Metodo AnularDocumentoCompra (INT 11)
    - Proposito: Realizar la anulacin formal de un requerimiento o solicitud de compra dentro del ERP una vez que ha sido procesado en FulllStep
    - Componente core: invocacion de **PR_ERP_COM_QRY_N_AnularReqCompra**
    - Funcion: asegura que el estado del documento refleje la anulacion en las tablas maestras de Big Magic para liberar presupuesto o registros
12. Metodo registrarOrdenCompra (INT 12)
    - Proposito: Generar fisicamente el orden de compra (OC) en el ERP a partir de la adjudicacion confirmada en fullstep
    - Componente core : Invoca **PR_ERP_COM_QRY_GN_RegistrarOrdenCompra**
    - Importancia: Es el paso donde el compromiso financiero se oficializa en el sistema contable de AJE
13. Metodo CancelarOrden
    - Proposito: Procesar la cancelacion de una orden de compra ya generada
    - Componente Core: invocacion a **PR_ERP_COM_QRY_GN_RegistrarOrdenCompra**
    - Detalle: ESte metodo es critico para la gestion de errores o cambios de ultimo momento en el suministro, notificando al ERP que la OC ya no debe ser procesada para la recepcion o pago
