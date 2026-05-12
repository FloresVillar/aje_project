### Doc Integraciones Salesforce.docx

#### Diseño funcional-técnico AJE

##### DT – Integración Salesforce AJE

**Control de Versiones**


| Versión | Autor | Fecha | Descripción | Revisor | Aprobador |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Elson Caldas | 02/08/2022 | | <Nombre> <br> <Fecha revisión> | <Nombre> <br> <Fecha Aprobación> |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

#### 1. Contenido del documento

1.  **Contenido del documento** **2**
2.  **Codificación del documento** **4**
3.  **Introducción** **5**
    *   3.1. *Necesidad identificada* 5
    *   3.2. *Objetivos del documento* 5
4.  **Diseño Técnico – Funcional (FTD)** **6**
    *   4.1. *Diseño de la solución* 6
    *   4.2. *Diagrama de secuencia* 6
        *   4.2.1. Pedido 6
        *   4.2.2. Salesforce 6
        *   4.2.3. Prospectos 6
        *   4.2.4. Clientes 6
        *   4.2.5. Módulos 6
        *   4.2.6. Stock Piso 6
        *   4.2.7. Estructura comercial 6
        *   4.2.8. Cuadre liquidación 6
        *   4.2.9. Carga técnica 6
        *   4.2.10. Calcular impuesto 6
        *   4.2.11. Autoventa 6
        *   4.2.12. Asignación módulo 6
    *   4.3. *Arquitectura AWS* 7
5.  **Especificación de Objetos** **9**
6.  **Objetos AWS** **11**
    *   6.1. *LAMBDAS* 11
        *   6.1.1. LAMBDA: login 11
        *   6.1.2. LAMBDA: createpedido 12
        *   6.1.3. LAMBDA: createprospecto 12
        *   6.1.4. LAMBDA: createcliente 13
        *   6.1.5. LAMBDA: createEstructuraCom 14
        *   6.1.6. LAMBDA: createModulo 14
        *   6.1.7. LAMBDA: createLP 15
        *   6.1.8. LAMBDA: createAsignacionModulo 16
        *   6.1.9. LAMBDA: createCargaTecnica 16
        *   6.1.10. LAMBDA: createCuadreLiquidacion 17

[Página] 2 / 38

        6.1.11. LAMBDA: createAutoventa 17
        6.1.12. LAMBDA: sincronizarpedido 18
        6.1.13. LAMBDA: salesforce 18
        6.1.14. LAMBDA: soapinvoker 20
        6.1.15. LAMBDA: restinvoker 21
        6.1.16. LAMBDA: actualizaData 22
        6.1.17. LAMBDA: query 23
        6.1.18. LAMBDA: stockPiso 23
        6.1.19. LAMBDA: calculaImpuesto 24
7. **Objetos BIG MAGIC** **25**

[Página] 3 / 38

#### 2. Codificación del documento


| Codificación del Documento | Valor |
| :--- | :--- |
| COD Trabajo | |
| Descripción Trabajo | |
| Área de Negocio | |
| Macroproceso | |
| Proceso | Producción |
| Subproceso | |
| Origen | |
| Motivo | |
| Tecnologías | |
| Versionado (1, 2, 3, ...) | 1 |

[Página] 4 / 38
#### 3. Introducción

##### 3.1. Necesidad identificada

##### 3.2. Objetivos del documento

El objetivo de este documento es definir los cambios para obtener la nueva funcionalidad.

[Página] 5 / 38

#### 4. Diseño Técnico – Funcional (FTD)

##### 4.1. Diseño de la solución

##### 4.2. Diagrama de secuencia

###### 4.2.1. Pedido 

**Diagrama de Secuencia de Integración:**
```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC

       |                |               |                |               |
       | Insertar pedido|               |                |               |
       |--------------->|               |                |               |
       |                | Insertar pedido                |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                | Procesar pedido                |               |
       |                |-------+       |                |               |
       |                |       |       |                |               |
       |                |<------+       |                |               |
       |                |        Obtener pedido si es grande             |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |        Insertar pedido XML     |               |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```
###### 4.2.2. Salesforce

**Diagrama de Secuencia de Integración (Salesforce):**

```bash
   Big Magic       AWS Lambda        AWS SQS          AWS S3         Salesforce


       |                |               |                |               |
       |  Enviar data   |               |                |               |
       |--------------->|               |                |               |
       |                | Insertar mensaje               |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                | Procesar mensaje               |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                |      Obtener JSON grandes      |               |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |          Enviar data           |               |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |Actualizar OUTBOX               |                |               |
       |<---------------|               |                |               |
       |   respuesta    |               |                |               |
       |--------------->|        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

[Página] 7 / 38

###### 4.2.3. Prospectos

**Diagrama de Secuencia de Integración (Prospectos):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         Salesforce



       |                |               |                |               |
       | Crear prospecto|               |                |               |
       |--------------->|               |                |               |
       |                | Insertar prospecto             |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                | Procesar prospecto             |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                |   Obtener prospec si es grande |               |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |     Insertar prospecto XML     |               |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

[Página] 8 / 38

###### 4.2.4. Clientes

**Diagrama de Secuencia de Integración (Clientes):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC




       |                |               |                |               |
       |  crear cliente |               |                |               |
       |--------------->|               |                |               |
       |                | Insertar cliente               |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                | Procesar cliente               |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                |   Obtener cliente si es grande |               |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |      Insertar cliente XML      |               |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

[Página] 9 / 38

###### 4.2.5. Módulos

**Diagrama de Secuencia de Integración (Módulos):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC


       |                |               |                |               |
       |  crear módulo  |               |                |               |
       |--------------->|               |                |               |
       |                | Insertar Modulo               |                |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                | Procesar Modulo               |                |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                |   Obtener Modulo si es grande |                |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |      Insertar Modulo XML      |                |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

###### 4.2.6. Stock Piso

[Página] 10 / 38

**Diagrama de Secuencia de Integración (Stock Piso):**

```bash
   Salesforce      AWS Lambda        Big Magic



       |                |               |
       |Obtener Stock piso              |
       |--------------->|               |
       |                |Obtener Stock piso
       |                |-------------->|
       |                |   respuesta   |
       |   respuesta    |<--------------|
       |<---------------|               |
       |                |               |
```

###### 4.2.7. Estructura comercial

**Diagrama de Secuencia de Integración (Estructura Comercial):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC



       |                |               |                |               |
       |Insertar Estructura comercial    |                |               |
       |--------------->|               |                |               |
       |                |Insertar Estructura comercial   |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                |Procesar estructura comercial   |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                | Obtener estructura comercial si es grande      |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |   Insertar Estructura comercial XML            |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

[Página] 11 / 38

###### 4.2.8. Cuadre liquidación

**Diagrama de Secuencia de Integración (Cuadre liquidación):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC



       |                |               |                |               |
       | Insertar cuadre|               |                |               |
       |--------------->|               |                |               |
       |                | Insertar cuadre                |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                | Procesar cuadre                |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                |   Obtener cuadre si es grande |                |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |      Insertar cuadre XML      |                |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

[Página] 12 / 38

###### 4.2.8. Carga tecnica
###### 4.2.9. Carga técnica

**Diagrama de Secuencia de Integración (Carga técnica):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC


       |                |               |                |               |
       | Insertar carga tecnica         |                |               |
       |--------------->|               |                |               |
       |                | Insertar carga tecnica         |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                | Procesar carga tecnica         |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                |  Obtener carga tecnica si es grande            |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |   Insertar carga tecnica XML   |               |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```

###### 4.2.10. Calcular impuesto

**Diagrama de Secuencia de Integración (Calcular impuesto):**

```bash
   Salesforce      AWS Lambda        Big Magic


       |                |               |
       |Calcular impuesto               |
       |--------------->|               |
       |                |Calcular impuesto
       |                |-------------->|
       |                |   respuesta   |
       |   respuesta    |<--------------|
       |<---------------|               |
       |                |               |
```

[Página] 14 / 38

###### 4.2.12. Asignación módulo

**Diagrama de Secuencia de Integración (Asignación módulo):**

```bash
   Salesforce      AWS Lambda        AWS SQS          AWS S3         BIG MAGIC



       |                |               |                |               |
       |Insertar asignación modulo       |                |               |
       |--------------->|               |                |               |
       |                |Insertar asignación modulo      |               |
       |                |-------------->|                |               |
       |                |   respuesta   |                |               |
       |   respuesta    |<--------------|                |               |
       |<---------------|               |                |               |
       |                |               |                |               |
       |                |Procesar asignación modulo      |               |
       |                |<--------------|                |               |
       |                |               |                |               |
       |                | Obtener asignación modulo si es grande         |
       |                |------------------------------->|               |
       |                |           respuesta            |               |
       |                |<-------------------------------|               |
       |                |               |                |               |
       |                |   Insertar asignación modulo XML               |
       |                |----------------------------------------------->|
       |                |           respuesta            |               |
       |                |<-----------------------------------------------|
       |                |               |                |               |
       |                |        Eliminar JSON si fue procesado          |
       |                |------------------------------->|               |
       |                |               |                |               |
```
##### 4.3. Arquitectura AWS

Para la integración, se desplegará la siguiente arquitectura:

```bash
[ INTEGRACIÓN AJE SALESFORCE - AWS - BIG MAGIC ]

  EXTERNO (Internet)          AWS COMERCIAL DESARROLLO (VPC)                ON-PREMISE (IBM)
 +--------------+        +-----------------------------------------+      +----------------+

 |              |        |  [ API Gateway ] <---> [ Cognito ]      |      |                |
 |  SALESFORCE  | <----> |        |                                |      |   FORTINET     |
 |              |        |  [ Lambda: Login ]                      |      |      |         |
 +--------------+        |        |                                |      |   [ VPN ]      |

                         |  +-----------------------------------+  |      |      |         |
       ^                 |  |  GRUPO LAMBDAS DE PROCESAMIENTO   |  |      | [ Big Magic ]  |

       |                 |  | (createpedido, createcliente,     |  |      |   (Database)   |
       |                 |  |  createModulo, createprospecto,   |  |      +----------------+
       |                 |  |  createLP, createAutoventa, etc.) |  |               ^
       |                 |  +-----------------------------------+  |               |
       |                 |        |                |               |               |
       |                 |  [ SQS: AJEColas ] <--> [ S3 Buckets ]  |               |
       |                 |        |                |               |               |
       |                 |  [ Lambda: sincronizarpedido ] ---------|---------------|
       |                 |        |                                |               |
       |                 |  +-----------------------------------+  |               |
       +-----------------|--|  [ Lambda: salesforce ]           |  |               |

                         |  +-----------------------------------+  |               |
                         |        |                                |               |
                         |  +-----------------------------------+  |               |
                         |  |  COLAS DE MENSAJERÍA (SQS)        |  |               |
                         |  |  (Q_REST_INVOKER, Q_SOAP_INVOKER, |  |               |
                         |  |   Q_DATA_UPDATE)                  |  |               |
                         |  +-----------------------------------+  |               |
                         |        |                                |               |
                         |  [ Lambdas: restinvoker, soapinvoker,|  |               |
                         |    actualizaData, query ] -----------|---------------|
                         +-----------------------------------------+

 [ Monitoreo ]           [ Infraestructura como Código ]
 - Amazon CloudWatch     - AWS CloudFormation (Templates)
```

**Componentes Principales Identificados:**
*   **API Gateway / Cognito:** Puerta de enlace segura y autenticación para las peticiones de Salesforce.
*   **VPC Private Subnet:** Entorno aislado para la ejecución de funciones Lambda de negocio.
*   **SQS (AJEColas):** Desacoplamiento de procesos mediante colas de mensajes.
*   **S3 Buckets:** Almacenamiento persistente para payloads de gran tamaño (JSON/XML).
*   **VPN / Fortinet:** Túnel seguro para la comunicación con la base de datos **Big Magic** en el datacenter de IBM.




| Servicio AWS | DESCRIPCIÓN |
| :--- | :--- |
| | |

| Servicio AWS | DESCRIPCIÓN |
| :--- | :--- |
| **Lambda** | <ul><li>createpedido</li><li>login</li><li>sincronizarpedido</li><li>salesforce</li><li>soapinvoker</li><li>restinvoker</li><li>createprospecto</li><li>createcliente</li><li>actualizaData</li><li>query</li><li>stockPiso</li><li>calculaImpuesto</li><li>createEstructuraCom</li><li>createModulo</li><li>createLP</li><li>createAsignacionModulo</li><li>createCargaTecnica</li><li>createCuadreLiquidacion</li><li>createAutoventa</li></ul> |
| **SQS** | <ul><li>Q_REST_INVOKER</li><li>Q_SOAP_INVOKER</li><li>Q_DATA_UPDATE</li></ul> |

[Página] 19 / 38


| CLOUDWATCH | guardado de logs internos |
| :--- | :--- |
| **DynamoDB** | Guardar calendarios |
| **S3** | <ul><li>Despliegue de proyecto serverless</li><li>Mensajes grandes</li></ul> |

[Página] 20 / 38

#### 5. Especificación de Objetos


| Código Funcionalidad | Descripción Funcionalidad | Grupo de Diseño |
| :--- | :--- | :--- |
| | | |

| Tipo de Objeto | Nombre | Acción: Crear | Acción: Modificar | Acción: Inactivar |
| :--- | :--- | :---: | :---: | :---: |
| Lambda Java | createpedido | ☑ | | |
| Lambda Java | login | ☑ | | |
| Lambda Java | sincronizarpedido | ☑ | | |
| Lambda Java | salesforce | ☑ | | |
| Lambda Java | soapinvoker | ☑ | | |
| Lambda Java | restinvoker | ☑ | | |
| Lambda Java | createprospecto | ☑ | | |
| Lambda Java | createcliente | ☑ | | |
| Lambda Java | actualizaData | ☑ | | |
| Lambda Java | query | ☑ | | |
| Lambda Java | stockPiso | ☑ | | |
| Lambda Java | calculaImpuesto | ☑ | | |
| Lambda Java | createEstructuraCom | ☑ | | |
| Lambda Java | createModulo | ☑ | | |
| Lambda Java | createLP | ☑ | | |
| Lambda Java | createAsignacionModulo | ☑ | | |
| Lambda Java | createCargaTecnica | ☑ | | |
| Lambda Java | createCuadreLiquidacion | ☑ | | |
| Lambda Java | createAutoventa | ☑ | | |
| SQS | AJEColas | ☑ | | |
| SQS | Q_REST_INVOKER | ☑ | | |
| SQS | Q_SOAP_INVOKER | | | |
| SQS | Q_DATA_UPDATE | ☑ | | |
| S3 | bucket-s3-aje-dev | | | |
| SP | COM_SALESFORCE_INSERTA_ERROR | ☑ | | |
| SP | COM_SALESFORCE_VALORIZAR_DOCUMENTOS | ☑ | | |
| SP | USP_SF_INVENTARIO_PISO_OBTENER | ☑ | | |
| Tabla | AJE_SF_OUTBOX | ☑ | | |
| Tabla | AJE_SF_INBOX | ☑ | | |

**Comentario:**
(Espacio vacío en el documento original)

[Página] 21 / 38

| Pruebas unitarias e integradas | |
| :--- | :--- |
| **Ejemplo** | |

[Página] 22 / 38

#### 6. Objetos AWS

##### 6.1. LAMBDAS

###### 6.1.1. LAMBDA: login

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "login" <br> Método: "Post" |

Función Lambda que permite obtener el token de autenticación para las demás funciones LAMBDA. La autenticación es mediante COGNITO.

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:


| Propiedad | Descripción |
| :--- | :--- |
| **username** | Usuario |
| **password** | contraseña |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Descripción |
| :--- | :--- |
| **accessToken** | |
| **expiresIn** | Tiempo de vida del token |
| **tokenType** | |
| **refreshToken** | |
| **idToken** | Token con el que podemos autenticarnos |
| **newDeviceMetadata** | |

###### 6.1.2. LAMBDA: createpedido

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "pedidos" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

*(Icono: Ejemplo trama pedido.json)*

La información recibida es insertada en la cola:


| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.3. LAMBDA: createprospecto

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "prospectos" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:



| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:



| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.4. LAMBDA: createcliente

**Desencadenadores:**



| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "clientes" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:



| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:



| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

[Página] 25 / 38

| message | Procesando informacion enviada. |
| :--- | :--- |

###### 6.1.5. LAMBDA: createEstructuraCom

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "estructurasComerciales" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:


| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.6. LAMBDA: createModulo

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |

| http | Ruta: "modulos" <br> Método: "Post" |
| :--- | :--- |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:


| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.7. LAMBDA: createLP

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "listasPrecio" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:


| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

[Página] 27 / 38

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.8. LAMBDA: createAsignacionModulo

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "asignacionesModulo" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:


| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.9. LAMBDA: createCargaTecnica

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "cargasTecnica" <br> Método: "Post" |

[Página] 28 / 38

| Método: "Post" | |
| :--- | :--- |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:



| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:



| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.10. LAMBDA: createCuadreLiquidacion

**Desencadenadores:**



| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "cuadreLiquidacion" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:



| Cola | Mensaje |
| :--- | :--- |


| AJEColas | Sin atributos |
| :--- | :--- |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:



| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.11. LAMBDA: createAutoventa

**Desencadenadores:**



| evento | Propiedades Evento |
| :--- | :--- |
| http | Ruta: "venta" <br> Método: "Post" |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:

La información recibida es insertada en la cola:



| Cola | Mensaje |
| :--- | :--- |
| **AJEColas** | Sin atributos |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:



| Propiedad | Valor |
| :--- | :--- |
| **message** | Procesando informacion enviada. |

###### 6.1.12. LAMBDA: sincronizarpedido

**Desencadenadores:**

[Página] 30 / 38


| evento | Propiedades Evento |
| :--- | :--- |
| **sqs** | Cola: AJEColas <br> Tamaño de lote: 1 |

Se inserta la data recibida en la tabla **AJE_SF_INBOX** en formato XML.

###### 6.1.13. LAMBDA: salesforce

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| **http** | Ruta: "salesforce" <br> Método: "Post" |

La información recibida es insertada en una de las siguientes colas:


| Cola | Mensaje |
| :--- | :--- |
| **Q_REST_INVOKER** | Sin atributos |
| **Q_SOAP_INVOKER** | Sin atributos |

En el cuerpo (Body) de la consulta deberá ser de tipo "raw -JSON (application/json)" y enviar la siguiente información:
{
  "id": "583568",
  "claveunica": "Codigo_unico__c",
  "pais": "PE",
  "compania": "0009",
  "accion": "1001",
  "xml": ""
}

si "**accion**" tiene como valor "**1000**" se almacena en la cola **Q_SOAP_INVOKER**
si "**accion**" tiene como valor "**1001**" o "**1002**" se almacena en la cola **Q_REST_INVOKER**

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:


| Propiedad | Valor |
| :--- | :--- |
| **message** | Trama enviada a Salesforce... |

###### 6.1.14. LAMBDA: soapinvoker

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| **sqs** | Cola: **Q_SOAP_INVOKER** <br> Tamaño de lote: 1 |

Envía a Salesforce la información recibida:
{

  "id": "406",
  "claveunica": "Codigo_unico__c",
  "pais": "CM",
  "compania": "0153",
  "accion": "1000",
  "xml": ""
}

Y como datos de respuesta desde salesforce se obtendrá un objeto JSON con la siguiente información:
{
  "compania": "0153",
  "id": "406",
  "message": "a0nS0000005qi8jIAA",
  "status": "9",
  "pais": "CM"
}

Envía la respuesta de Salesforce a la siguiente cola:



| Cola | Mensaje |
| :--- | :--- |
| **Q_DATA_UPDATE** | Sin atributos |

###### 6.1.15. LAMBDA: restinvoker

**Desencadenadores:**



| evento | Propiedades Evento |
| :--- | :--- |
| **sqs** | Cola: **Q_REST_INVOKER** <br> Tamaño de lote: 1 |

Envía a Salesforce la información recibida:
{
  "id": "12162302",
  "accion": "1001",
  "claveunica": "Codigo_unico__c",
  "xml": "",
  "pais": "PE",
  "compania": "0022"
}

Y como datos de respuesta desde salesforce se obtendrá un objeto JSON con la siguiente información:
{
  "status": "1",
  "rows": "0",
  "message": "System.QueryException: List has no rows for assignment to SObject",
  "errors": [
    "List has no rows for assignment to SObject - Línea 45"
  ]
}

Envía la respuesta de Salesforce a la siguiente cola:



| Cola | Mensaje |
| :--- | :--- |
| **Q_DATA_UPDATE** | Sin atributos |

###### 6.1.16. LAMBDA: actualizaData

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| **sqs** | Cola: **Q_DATA_UPDATE** <br> Tamaño de lote: 1 |

se obtendrá un objeto JSON con la siguiente información:

{
  "compania": "0153",
  "id": "406",
  "message": "a0nS0000005qi8jIAA",
  "status": "9",
  "pais": "CM"
}

**Actualiza el contenido de la tabla AJE_SF_OUTBOX**

**Ejecuta SQL MAGIC de la tabla AJE_SF_OUTBOX**

**En caso el mensaje tenga un status diferente de "9" se ejecuta el procedimiento almacenado COM_SALESFORCE_INSERTA_ERROR**

###### 6.1.17. LAMBDA: query

**Desencadenadores:**

| evento | Propiedades Evento |
| :--- | :--- |
| **http** | Ruta: "query" <br> Método: "Post" |

Ejecuta QUERY en Salesforce:



| Entidad | query |
| :--- | :--- |
| AVANCEDIA | SELECT Codigo_Vendedor__c,Compania__c,Fecha__c,Fin_de_dia__c, Inicio_de_dia__c,Nombre_Vendedor__c,Pais__c,RutaN__c,Sucursal__c, Vendedor_volante__c,ZonaN__c FROM Avance_del_dia__c WHERE Pais__c = '%s' and Fecha__c >= %s AND Compania__c = %s |
| INVENTARIO | SELECT Inventario__r.Cliente__r.Compania__r.Codigo__c, Inventario__r.Cliente__r.Compania__r.Pais__c, Inventario__r.Fecha__c, Inventario__r.Cliente__r.Codigo_Cliente__c, Codigo_de_SKU__c, Cantidad__c FROM Entrada_de_inventario__c WHERE Inventario__r.Cliente__r.Compania__r.Pais__c = '%s' AND Inventario__r.Fecha__c = TODAY |

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:



| Propiedad | Valor |
| :--- | :--- |
| **message** | XML información |

###### 6.1.18. LAMBDA: stockPiso

**Desencadenadores:**



| evento | Propiedades Evento |
| :--- | :--- |
| **http** | Ruta: "stockPiso" <br> Método: "Post" |

Ejecuta el SP **USP_SF_INVENTARIO_PISO_OBTENER** en BIG MAGIC.

[Página] 36 / 38

###### 6.1.19. LAMBDA: calculaImpuesto

**Desencadenadores:**


| evento | Propiedades Evento |
| :--- | :--- |
| **http** | Ruta: "calculaImpuesto" <br> Método: "Post" |

Ejecuta el SP **COM_SALESFORCE_VALORIZAR_DOCUMENTOS** en BIG MAGIC.

Y como datos de respuesta se obtendrá un objeto JSON con la siguiente información:

{
  "documento": {
    "cliente": 413980,
    "compania": "0153",
    "detalles": "",
    "pais": "CM"
  }
}

[Página] 37 / 38
#### 7. Objetos BIG MAGIC

##### 7.1. SP: COM_SALESFORCE_INSERTA_ERROR

EL SP es ejecutado por la función lambda “actualizaData”.
Inserta errores de las solicitudes de Salesforce en la tabla **AJE_SF_ERROR**

##### 7.2. SP: COM_SALESFORCE_VALORIZAR_DOCUMENTOS

El SP es ejecutado por la función lambda “calculaImpuesto”.
Valoriza los documentos 'FXC' y 'BOL' en línea enviados desde SALESFORCE

##### 7.3. SP: USP_SF_INVENTARIO_PISO_OBTENER

El SP es ejecutado por la función lambda “stockPiso”.

[Página] 38 / 38


