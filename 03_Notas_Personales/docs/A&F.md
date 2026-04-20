Documentacion parafraseado del buen gemini.

## FullStep

### Integracion proceso compras
Es la "pieza hermana" del plan de viajes , pero enfocada a Compras y abastecimiento. Aqui se ve como se integra la plataforma externa FullStep (Saas de e-procurement) con el ecosistema de AJE.

#### FullStep como SaaS
está al lado izquierdo ,aparece como SaaS , es la plataforma donde los compradores de AJE probablemente gestionan licitaciones , cotizaciones y seleccion de proveedores.

- la conexion : se comunica via **Web Services** con un servidor **WildFly** (un servidor de aplicacion Java) que está en la nube de AWS de AJE.

#### Compras Metodos SOAP
Se ve el desglose WSDL para **ComprasAJE-fullSetpv3**, aqui es donde ocurre la integración,los metodos se dividen en 3 funciones que impactan al ERP:
- Anulacion o baja: **cancelarOrden** o **anularDocumentoCompra**

- Consulta: métodos **consultarProveedor** o **listarPartidasPresupuestarias** , el sistema de compras preguntan al ERP ¿tenemos dinero en esta cuenta? ¿este proveedor existe?

- Insercion: **registrarOrdenCompra** y **registrarAdjudicacion** cuando fullstep termina un proceso de compra, empuja la orden de compra terminada hacia el ecosistema de AJE para que se convierta en un compromiso financiero.

#### Destino de los datos : AWS BM (base de datos)

A la derecha del diagrama de AWS se ve el bloque AWS BM con multiples bases de datos por el pais:
- BD MX (10.101.6.184) Mexico
- BD PERU (10.101.10.143) Peru

Lo destacable es que el servidor **WildFly** actúa como un **Hub**. Recibe la informacion de FullStep y, segun el pais que este comprando, distribuye la informacion a la base de datos del ERP Big Magic.

Como se conecta esto con el **Plan de viajes**  :
- validacion: asi como el plan de viajes valida empleados, aqui se validan proveedores y presupuestos
- Cierre contable: el plan de viajes genera una OG , este sistema genera una OC , ambas se registran en el mismo core (Big Magic)
- Arquitectura hibrida: Ambos usan SOAP(xml) para comunicar nubes externas(Azure en compras,fullstep en compras) con la red privada de AJE (10.x.x.x).

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

[detalle de las red]()

## SAP MX

### Flujo Macro: Administracion del personal

Un diagrama de procesos de negocio se organiza mediante pool(todo el cuadro), lanes(divisiones horizontales), eventos(circulos verde rojo) y comuertas (rombos ,desiciones)

**Procesos macro proyecto apolo** , muestra un modelo basado en  BPMN2.0(Diagrama de procesos de negocio) , este define la interaccion entre los diferentes roles de  regionales(BO,PE,CO,MEX, etc). Este flujo es critico pues determina el origen de los datos que alimentan la tabla MPERSOEF en el core legacy.

<p align="center">
    <img src="../../imagenes/BPMN.png" width="80%">
</p>

Como se mencionó es un diagrama de procesos de negocios. Tiene por proposito definir el gobierno de dato, antes de que un bit se escriba en el AS400 o en SAP ,debe haber una aprobacion humana.

En este caso se basa en el ciclo de vida del empleado (Employee Lifecycle Management) , se mapea el Onboarding(gestion de contrato) hasta el offboarding(desvinculación ). 

Aterricemos de tanta teoria, el diagrama es suficientemente explicita, precisemos sus detalles:

Se disponene de 3 lanes 

- **analista/coordinador de TH**
- **Coordinador de talento humano**
- **jee inmediato del area usuaria**

En el primero se ubica el evento iniciar, el cual es seguido de una acccion que simplemente indica que el flujo se bifurca, merced a una  comuerta paralela(rombo/comuerta con el signo +) .  Uno de los destinos es el subproceso colapsado(+ los detalles estan en otro diagrama) de nombre **Gestion de contrato**.
El otro destino es el subprceso colapsado **Gestion Laboral** en el tercer lane.

**"En gestion de contrato de personal y registro de informacion"**, el flujo a un evento intermedio(circulo hueco ) , luego este sigue el flujo a un subproceso **gestion de tiempo**, el flujo encuentra  una comuerta exclusiva (rombo con una X); la desicion que se toma es respecto a ¿ausencia del trabajador? .
Si el trabajador esta ausente se nos direcciona al subproceso **Gestion de ausencia**. 

Una vez realizado la inspeccion de la presencia del trabajador , se llega a la comuerta basada en eventos donde el usuario no toma la desicion, sino que esta depende de que sucede antes. Seguidamente bifurcammos en dos eventos intermedios. El primer evento es **necesidad de actualizacion de datos** y el que le sigue es **requirimiento de movimiento**. Ocurrido estos estos eventos hacen aparacion los subprocesos **Gestionar los datos de los empleados** y **Gestion de movimientos de puestos de trabajo** ,ambos son subprocesos colapsados.Realizados cada uno de ellos, la comuerta exclusiva  redirige el el flujo hacia el evento **Necesidad de desvinculacion** .LE sigue el subproceso **Gestion de desvinculacion**.

Luego una comuerta exclusiva en el que confluye parte de la bifurcacion hecha al inicio (la que estamos analizando) y otra que se dirigio al lane **jefe inmediato del area usuaria**.Es este ultimo lane se realiza el subproceso **Gestion laboral**.

Finalmente el comutador exclusivo conviene en el evento final , el de color rojo.



### Flujo Macro: Gestion de Nomina

El nombre del pool es gestion de nomina, se observan cuatro lanes :
- **Analista de nomina**
- **Coordinador de talento humano**
- **Jefe de talento humano**
- **Gerencia TH**
<p align="">
    <img src="../../imagenes/nomina.png" width="80%">
</p>
Una vez detallado la teoria en TECH_NOTES.md y aqui mismo, es factible leer el diagrama de procesos.


Detallemos sin embargo el diagrama. 

Gestion de nomina trata sobre "cuando y cuanto se paga", mientras que el macro administracion de personal trataba  de "quien entra y quien sale".

Los roles y lanes (roles y responsabilidades)constituyen un proceso jerarquico, se aprecia un flujo de arriba hacia abajo , para las **operaciones** y para los **reportes** respectivamente.
**Analista de nomina** es el operador, recopila novedades (horas extra, faltas que provienen del macro anterior). <br>
**Coordinador de talentos** es el validador intermedio.En tanto que **jeffe de talento humano** y **Gerencia TH** son el auditor y aprobadores finales (quien da la orden de liberar el pago en el banco) respectivamente.

Inspeccionando la simbologia se aprecia algo nuevo, el evento tiempo que es **evento intermedio temporal(timer event)** el cual indica que el evento no se debe a una accion humana sino a una fecha especifica. Lo cual en SAP (odoo) se traduce en un **batch jobs** (una tarea programada).El sistema despierta solo cuando el calendariio de cierre lo precisa.

Luego la comuerta paralela , bifuca en **informe de fin de periodo e impuestos** (gobierno/entidades fiscales) y en **metricas y reportes al empleado** (boletas pago/desprendibles).

El sistema garantiza la integridad de la informacion post-pago mediante la ejecucion paralela de obligaciones fiscales y notificaciones al colaborador.

La conexion entre ambos diagramas , administracion y nomina se da del siguiente modo, **administracion de personal** genera los datos maestros (nuevos sueldos, baja, ausencia) y **gestion de nomina** toma estos datos y los transforma en dinero. La tabla MPERSOEF(**transversal/Extraccion ETL - Microsofft Fabrics/PROCESO DE EXTRACCION MICROSOFT FABRIC.docx**) en big magic es la que sirve de puente.Si el analista no activa el personal en el primer macro/diagrama , el analista de nomina no lo vera en el segundo.

Es preciso concluir con un pequeño resumen, la arquitectura de procesos de AJE separa **administracion de personal** de la **la gestion de nomina** , integrando ambas mediante hilos temporales(**Timer Events**) y el flujo de aprobacion multinivel para cumplir con la fiscalidad de cada pais (MX,PE,BO,...)




