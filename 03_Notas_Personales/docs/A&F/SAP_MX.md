
# SAP MX 

## Documentación de Procesos
**Transformación Digital / Talento Humano**

---

## Flujo Macro: Administración del Personal

### Roles por País

*   **BO:** Auxiliar de TH.
*   **PE, CO, MX, VE, EC y GLOBAL:** Analista de Talento Humano.
*   **Demás países:** Coordinador de TH / Analista de TH.

---

### Esquema del Proceso (BPMN ASCII)

```text
 ANALISTA / COORDINADOR TH          COORDINADOR TH            JEFE INMEDIATO
+--------------------------+      +------------------+      +----------------+

|                          |      |                  |      |                |
|  (O) Personal            |      |                  |      |                |
|      Seleccionado        |      |                  |      |                |
|        |                 |      |                  |      |                |
|        v                 |      |                  |      |                |
|      [ + ] ------------+ |      |                  |      |                |
|        |               | |      |                  |      |                |
|        v               | |      |                  |      |                |
|  [ Gestión de  ]       | |      |                  |      |                |
|  [ contrato y  ]       | |      |                  |      |                |
|  [ registro    ]       | |      |                  |      |                |
|        |               | |      |                  |      |                |
|        v               | |      |                  |      |                |
|  ( ) Personal          | |      |                  |      |                |
|      Activado          | |      |                  |      |                |
|        |               | |      |                  |      |                |
|        +---------------|--------|------------------|----> [ Gestión        ]
|                        | |      |                  |      [ Laboral        ]
|                        | |      |                  |      +-------+--------+
|                        | |      |                  |              |
|                        | |      |                  |              |
|                        | |      | [ Gestión de     ] <------------+
|                        | |      | [ tiempo         ]
|                        | |      | +-------+--------+
|                        | |      |         |
|                        | |      |         v
|                        | |      |      < Ausencia? > -- No --> (X)
|                        | |      |         |
|                        | |      |         Si
|                        | |      |         v
|                        | |      | [ Gestión de     ]
|                        | |      | [ ausencia       ]
|                        | |      | +-------+--------+
|                        | |      |         |
|         ^              | |      |         |
|         |              +-|------|---------+
|    < Requiere? >         |      |
|     /        \           |      |
|    v          v          |      |
|[ Gestión ]  [ Gestión  ] |      |
|[ de Datos]  [ de Mov.  ] |      |
|    |          |          |      |
|    v          v          |      |
|    +----------+          |      |
|         |                |      |
|         v                |      |
|    ( ) Necesidad de      |      |
|        Desvinculación    |      |
|         |                |      |
|         v                |      |
|    [ Gestión de     ]    |      |
|    [ desvinculación ]    |      |
|         |                |      |
|         v                |      |
|        (X) Fin           |      |
|                          |      |
+--------------------------+      +------------------+      +----------------+
```

### Descripción de Subprocesos Principales

1.  **Gestión de Contrato:** Registro de información inicial del personal local o extranjero.
2.  **Gestión Laboral:** Actividades coordinadas por el Jefe Inmediato del área usuaria.
3.  **Gestión de Tiempo y Ausencias:** Control de asistencia y manejo de faltas/permisos.
4.  **Mantenimiento:** Actualización de datos de empleados y movimientos de puestos.
5.  **Desvinculación:** Proceso final de salida de la organización.




 

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



## Flujo Macro: Gestion de Nomina

```bash
 ANALISTA NÓMINA         COORDINADOR TH          JEFE TH            GERENCIA TH
+-----------------+     +-----------------+     +-------------+     +-------------+


| (O) Inicio      |     |                 |     |             |     |             |
|      |          |     |                 |     |             |     |             |
| [ 1. Recopilar  ]     |                 |     |             |     |             |
| [ datos nómina  ]     |                 |     |             |     |             |
|      |          |     |                 |     |             |     |             |
+------|----------+     +-----------------+     +-------------+     +-------------+

       |                       ^
       v                       |
+-----------------+     +------|----------+     +-------------+     +-------------+

|                 |     | [ 2. Procesar   ]     |             |     |             |
|                 |     | [ datos nómina  ]     |             |     |             |
|                 |     |      |          |     |             |     |             |
+-----------------+     +------|----------+     +-------------+     +-------------+

                               |                       ^
                               v                       |
+-----------------+     +-----------------+     +------|----------+     +-------------+

|                 |     |                 |     | [ 3. Validar    ]     |             |
|                 |     |                 |     | [ datos nómina  ]     |             |
|                 |     |                 |     |      |          |     |             |
+-----------------+     +-----------------+     +------|----------+     +-------------+

                                                       |                       ^
                                                       v                       |
+-----------------+     +-----------------+     +-----------------+     +------|------+

|                 |     |                 |     |                 |     | [ 4. Aprobar ]
|                 |     |                 |     |                 |     | [ y pagar    ]
|                 |     |                 |     |                 |     |      |       |
+-----------------+     +-----------------+     +-----------------+     +------|------+

                                                                               |
                               +-----------------------------------------------+
                               |
                               v
+-----------------+     +------------+----------+     +-------------+     +-------------+

|                 |     |            |          |     |             |     |             |
|                 |     |      < [ + ] >        |     |             |     |             |
|                 |     |       /     \         |     |             |     |             |
|                 |     | (L) Cierre   (L) Pago |     |             |     |             |
|                 |     |  |            |       |     |             |     |             |
|                 |     |  v            v       |     |             |     |             |
|                 |     |[ 5. Informe ] [ 6. Métricas ]     |             |     |
|                 |     |[ impuestos  ] [ y reportes ]     |             |     |
|                 |     |  |            |       |     |             |     |             |
|                 |     |  \          /         |     |             |     |             |
|                 |     |      < [ + ] >        |     |             |     |             |
|                 |     |          |            |     |             |     |             |
|                 |     |         (X) Fin       |     |             |     |             |
+-----------------+     +-----------------------+     +-------------+     +-------------+

```

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

### 20260306 - Py Lego MX - SAP Nómina v1.0
Se detalla la capa tecnica de servicios que permite que SAP se comunique con el Core Legacy y otros sistemas satelites.
- APlicacion satelite/proveedor: Identifica al sistema que interactua con el core(SAP NOMINA) y al consultor responsable de la implementacion(EPIUSE)
- Proceso/Integracion : Define el objeto de negocio que se mueve (empleaddos, centro de consto, acreedores o asiento)  y el nombre asignado al flujo en AWS (ej: ajegroup-aws-rrhh-prod-InsertarUsuarios)
- Descripcion/Metodo: Explica el flujo logico(quien le envia a quien) y protocolo de transporte.Nota que mientras los empleados usan API (comunicacion directa) los demas usan SFTP (intercambio de archivos planos)
- Tipo Accion : En todos los casos es insert, lo que indica que estas integraciones estan diseñadas para crear o registrar nuevos registros en el sistema de destino , no solo para consulta.
- Emisor/Destino: Establece la jerarquia del dato
    - Para empleados y Asientos: SAP es una fuente de verdad (Emisor)
    - Para centros de costo y acreedores, el core legacy (big magic) manda la informacion hacia el SAP
- Frecuencia/Disparador: Determina la periocidad y la tecnologia de ejecucion. Todos los flujos son orquestados por AWD lambda, pero con ritmos distintos , desde alta frecuencia (cada 1 hora  para empleados) hasta procesos nocturnos (8 pm) o de cierre (12 pm  y 6 am)
- Endpoints (TEST/PROD) : son las direcciones fisicas(urls) donde se enchufan los servicios.Diferencian el ambiente de pruebas(api19preview) del entorno real de produccion (api19)
- SP/ Triggeer Relacionados: Es el componente de base de datos que se activa al recibir el dato
    - En SQL server BM , se dispara el trigger **dbo.EMPLEADO_PROGRA_INS** para el personal o se inserta en la tabla fisica **TVOUCH24F** para la contabilidad
    - Para las extracciones desde BM, se usa un Stored Procedures especificos de finanzas  **PR_ERP_FNZ_QRY_GN**
```bash
+---------------------+-----------------+--------------------------+------------------------------------------------+

| Proceso             | Frecuencia      | Disparador (AWS Lambda)  | Componente DB Relacionado                      |
+---------------------+-----------------+--------------------------+------------------------------------------------+

| Empleados           | Cada 1 hora     | InsertarUsuarios         | Trigger [dbo].[EMPLEADO_PROGRA_INS]            |
| Centro de Costo     | Diaria (8 PM)   | InsertarCentroCostos     | PR_ERP_FNZ_QRY_GN_ObtenerDatosCCostoNomina     |
| Acreedores/Deudores | Diaria (8 PM)   | InsertarAcreedor         | PR_ERP_FNZ_QRY_GN_ObtenerDatosProveedoresNomina |
| Asiento Contable    | 12 PM y 6 PM    | InsertarAsientosContables| Tabla TVOUCH24F                                |
+---------------------+-----------------+--------------------------+------------------------------------------------+

```
