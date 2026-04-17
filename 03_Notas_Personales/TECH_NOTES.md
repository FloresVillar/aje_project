## Envoltorios creados por sistemas de compresion
**problema**<br>
Al descomprimir el .zip de la documentacion del proyecto  crea un "envoltorio", la carpeta con el ID de descarga y dentro contiene la estructura real.
**G:\CARPETAS\documentacion\CARPETAS\..**

Para disponer de una arbol de directorios limpio , con carpetas de naturalezas especificas. Necesitamos primero , renombrar est envoltorio y luego crear subcapetas para documentacion, pruebas y otros.

**desicion**<br>

**Anatomia de comandos PowerShell**.

La sintaxis verbo-Sustantivo **verb-noun** , powershell usa una estructura muy humana 
- Verbo : es la accion (Get, Set, Move, Remove)
- Sustantivo: EL objetivo sobre el que cae la accion(Item, ChildItem,Content)

- Parametros: Empiezan con un guion (-Path,-Destination).

**Move-Item -Path "ARCHIVO" -Destination ".."** , mueve el archivo ARCHIVO a la carpeta padre , .. indica que se sube un nivel.

En este caso espefico no se mueve el contenido de archivo o carpeta un nivel arriba de donde se esta.Sino que actualiza un puntero en la **tabla maestra MFT**,realizando algo parecido a 'actualiza quien es hijo de quien'.De modo que mover gb's dentro del mismo duro es facil, mas que moverlo a un usb.

**estado**<br>
```bash
(base) PS G:\Esau> Rename-Item -Path ".\Documentacion-20260407T153446Z-3-001" -NewName "Projecto_AJE"

Rename-Item : Acceso denegado a la ruta de acceso 'G:\Esau\Documentacion-20260407T153446Z-3-001'.
En línea: 1 Carácter: 1
+ Rename-Item -Path ".\Documentacion-20260407T153446Z-3-001" -NewName " ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : WriteError: (G:\Esau\Documen...7T153446Z-3-001:String) [Rename-Item], IOException
    + FullyQualifiedErrorId : RenameItemIOError,Microsoft.PowerShell.Commands.RenameItemCommand

```
**Consecuencias**<br>
Aun no es posible renombrar el archivo.Existen dos errores **WriteError** , para renombrar una carpeta ,se necesita permisos especificos para modificar o escribir atributos sobre el padre. Mas adelante se probara que este error no es el determinante.

## ERRORES DE EJECUCION DE COMANDO Rename-Item

**problema**<br>
Dos problemas, Write-Error y IOException,que no permiten cambiar el nombre a la carpeta. 

**desicion**<br>
- Se ejecuta el comando de obtencion de lista de control de acceso.
```bash
Get-Acl -Path "ARCHIVO/CARPETA" | Format-List

..  Allow  FullControl
         CREATOR OWNER Allow  FullControl ..
```
- Otra posible causa es que anaconda/conda tiene activado (base) el entorno virtual base de conda.Entoces conda ha inyectado una serie de rutas y scripts en la memoria para usar modulos python.El problema (segun parafraseando a gemini) es que conda activa servicios de indexacion o monitoreo. 
Si alguna vez se abrio un script python en esta carpeta , el proceso padre conda puede mantener un hilo de ejecucion mirando esa carpeta.
Se ejecuta 
```bash
conda deactivate
```
- SHL (System Handle Lock ) Bloqueo de nivel de sistema. Al descargar y extraer un .zip el explorador de archivos a menudo mantiene un hilo abierto. La ventan del explorador de archivos, para ser exactos. El proceso **explorer.exe** registra un handle de lectura. El proceso del explorador la tiene marcada como abierta para lectura de metadatos. Por lo cual cualquier intento de modificar el nombre (destruir el indice viejo y crear uno nuevo) falla con un **IOException**.

Entonces se ejecuta **windows + R** , y el monitor de recursos **resmon.exe** , seguidamente se busca en CPU - Identificadores asociados . Se identifica que este es el problema. CTRL + SHIFT + ESC y reiniciamos ese proceso.

Finalmente 
```bash
Rename-Item -Path "ARCHIVO/CARPETA" -NewName "NUEVO_NOMBRE" 
```

**estado**<br>
El comando Rename-Item y similares ahora ejecutan correctamente.

**consecuencias**<br>
Se continua con la familizacion del entorno powerShell. Resuelto en problema del Envoltorio creado por sistemas de comprension.

## Crear una estructura de trabajo

**problema**<br>
**Ordenamiento determinista** POr defecto los sistemas operativos ordenan los archivos y carpeta de forma alfabetica. Luego a medida que el proyecto crece, el agregar carpetas ccomo Scripts, Backups o Config, el orden alfabetico se vuelve un caos.

Una solucion intuitiva parece ser enumerar el orden del flujo de trabajo, asi se refleja un flujo mental que enumera (valga la redundancia) las etapas que seguimos.

**Recordar que se parafrasea la teoria que amablemente brinda gemini**.

Evitamos a su vez el anidamiento infinito . Windows tiene un limite de 260 caracteres para la ruta completa (MAX_PATH). Si nuestras carpetas tienen nombres larguisimos o se encuentarn en subcarpetas y subcarpetas. LLegará un punto en que sencillamente no se pueda abrir dicho archivo.

De modo que enumerar es una tecnica de abstraccion , convertimos un monton de archivos en un SISTEMA.


**desicion**<br>
Ejecutamos comando de creacion de carpetas , se precisa que el tipo de archivo -ItemType.

```bash
    New-Item -Path "01_Docs_oficiales" , "02_Entorno_Pruebas" , "03_Notas_Personales" -ItemType Directory
```
**estado**<br>
Resuelto
**consecuencias**<br>
Se solventa correctamente la creacion del sistema de archivos.Puesto que el sistema operativo reserva espacio en la MFT (maste file table) para estas nuevas entradas.

## ARQUITECTURA EN LA DOCUMENTACION 

**problema**<br>
Implementar una arquitectura de documentacion que obedezca al Knowledge Base (KB).

Para detallar cuanto se pueda y deba, un README.md se volvera extenso y dificil de digerir. 
**desicion**<br>
La respuesta es usa una carpeta de documentacion dentro de 03_Notas_Personales\docs\ y dentro de ella. **sintaxis-sql.md** para la teoria de stored procedures , **modulos-glue.md** arquitectura de aws , **glosario-aje.md** termino de negocios (A&F , Comercial)

Para el actual estado de la revision de la documentacion , no es tan grato implementar lo anterior, caso contrario la metodologia ADR (Arquitecture Desicion Rcords). Se crea un markdown **TECH_NOTES.md** donde se documenta 

- El problema
- Desicion
- Estado
- Consecuencias

**estado**<br>
Se implementa ADR
**consecuencias**<br>
Detalle de la sintaxis de los comandos powerShell para la creacion de un Sistema de archivos como tal.

## Emular el comportamiento de tree -L N 

**problema**<br>
Es util obtener una vista de la jerarquia de archivos, en linux se usaria **tree -L 5** ver los archivos con una profundidad de 5 . En windows existe un comando similar.
**desicion**<br>
Se ejecuta 
```bash
cmd /c "tree /f /a"
```
Desglosando la sintaxis, **cmd /c** levanta una instancia del procesador de comandos original. **tree**, es un ejecutable (tree.com) escrito en C que recorre el arbol de nodos del sistema de archivo de forma recursiva, manteniendo una pila en memoria. 
**/f** incluye archivos, **/a** para no ver simbolos raros en la terminal.

Ademas se puede redireccionar la salida  de este ultimo comando , mediante **Out-File -FilePath "ARCHIVO"**

```bash
cmd /c "tree /f /a" | Out-File "arbol_directorio.txt"       

```

**estado**<br>
Se solventa adecuadamente
**consecuencias**<br>
La jerarquia de archivos o arbol de directorios se observa gratamente.

## Creacion de un nuevo archivo

El problema es que se requiere crear un nuevo archivo, mas que decidirse , se aprende la sintaxis para ello.
```bash
New-Item -Path ".\ARCHIVO.txt" -ITemType "File"
```
El estado del problema se resuelve. 

## Emular un Makefile en windows
Se require un equivalente a Makefile.Para tal fin en powerShell creamos un **.ps1** , de nombre make. La sintaxis incluye una declaracion de interfaz param(bloque de parametros), este es el contrato que define los datos que recibirá el .\make desde el terminal.

Tambien se define [string] y los parametros mediante $command y $ARCHIVO. 

Luego **switch** es la estructura de control de flujos, es un comparador por lista. Toma el valor de $command recorre la la lista dentro de **{}** y busca el nombre que coincida con el argumento ingresado mediante .\make ARGUMENTO.

## Teoria acerca de los .wsdl y SOAP
Un WSDL (web services description language) es, un manual de instrucciones tecnico de un servicio web basado en SOAP.

Cuando un sistema necesita hablar con un servicor de AJE ,el archivo WSDL dice:
- Qué metodos existes (ej: validarEmpleado)
- Qué datos debo enviar (ej : un string para el nombre, un integer para el ID)
- Qué voy a recibir de vuelta (ej: codigo de exito)
- A donde enviar la peticion (la URL o endpoint del servicio)

Tiene etiquetas, entre las mas importantes:
- **< types >** : Define los tipos de datos(como un diccionario de variables)
- **< messages >** : Define los datos que entran y salen
- **< portType >** : Es la lista de operaciones 
- **< binding >** : Define el protocolo (HTTP) y el formato de mensajes
- **< services >** : La direccion fisica(URL) donde vive el servicio

Mientras que SOAP (Simple Object Access Protocol) es el "sobre" para enviar el contrato(.wsdl).
Es un protocolo de comunicacion que permite que dos sistemas intercambien informacion.Geralmente a traves de HTTP (en formato xml).

SOAP define la estructura exacta del .wsdl para que este no sea rechazado
- Envelope(Envoltorio) : La etiqueta raiz dice:"este es un mensaje SOAP"
- Header : Informacion adicional
- Body : contenido, se pide por ejemplo los datos de un empleado
- Fault: Si algo salio mal

Las 3 reglas de SOAP: 
- Solo XML : no usa json. Es un texto plano pero con etiquetas muy rigidas.
- Independiente : Si el servidor es windows y el cliente un contenedor linux, si ambos leen XMl, se entienden
- Neutralidad de transporte: aunque normalmente viaja por http, SOAP podria ser enviado via correo u otros medios.

comparando 

```bash
+-----------------+--------------------------------+-------------------------------+
| Característica  |  WSDL / SOAP (Plan de Viajes)  |   REST / JSON (Salesforce)    |
+-----------------+--------------------------------+-------------------------------+
| Formato         | XML estricto                   | JSON ligero                   |
+-----------------+--------------------------------+-------------------------------+
| Rigidez         | Muy alta (falla si falta algo) | Flexible                      |
+-----------------+--------------------------------+-------------------------------+
| Contrato        | WSDL (Contrato obligatorio)    | Opcional (Swagger/OpenAPI)    |
+-----------------+--------------------------------+-------------------------------+
| Uso común       | Sistemas bancarios, ERP, AJE   | Apps móviles, Web modernas    |
+-----------------+--------------------------------+-------------------------------+
| Protocolo       | Basado en Acciones (Verbos)    | Basado en Recursos (Nombres)  |
+-----------------+--------------------------------+-------------------------------+
| Transporte      | HTTP, SMTP, JMS, etc.          | Principalmente HTTP/HTTPS     |
+-----------------+--------------------------------+-------------------------------+
```
Ejemplos
```bash
+----------+--------------------------------+--------------------------------+
| Aspecto  |     SOAP (Plan de Viajes)      |    REST (Salesforce / Zuper)   |
+----------+--------------------------------+--------------------------------+
| Estilo   | Acción (Ej: ValidarUsuario)    | Recurso (Ej: /usuarios/123)    |
+----------+--------------------------------+--------------------------------+
| Verbos   | Casi siempre usa POST          | Usa GET, POST, PUT, DELETE     |
+----------+--------------------------------+--------------------------------+
| Peso     | Pesado (XML con mucho overhead)| Ligero (JSON optimizado)       |
+----------+--------------------------------+--------------------------------+
| Estado   | Stateful (puede mantenerlo)    | Stateless (sin estado)         |
+----------+--------------------------------+--------------------------------+
| Seguridad| WS-Security (Nivel Mensaje)    | HTTPS / OAuth (Nivel Canal)    |
+----------+--------------------------------+--------------------------------+
```
AJE usa SOAP y no algo mas moderno? 
- Seguridad: tiene estandares muy robustos (Ws-Security) 
- Transacciones: si un viaje se realiza a medias, se cancela
- Contrato seguro: gracias a wsdl , si el mensaje no es perfecto el servidor rebota.

```bash
<soap:Envelope xmlns:soap="http://www.w3.org">
    <soap:Header/>
        <soap:Body>
        <m:GetEmpleado>
        </GetEmpleado>
    </Body>
</soap:Envelope>
```

## Diagrama de procesos de Negocio

Un diagrama de proceso de negocio bajo el estandar BPMN 2.0 business protocol model and notation, es el lenguaje universal que usan los arquitectos de soluciones y analistas para que el equipo de IT y el de negocio hablen el mismo idioma.

Es un diagrama de flujo de procesos (BPMN) de nivel macro.Se organiza mediante:
- pool : El recuadro que contiene los demas elementos.
- Lanes(carriles): las divisiones horizontales que indica quien hace qué
- Eventos (circulos): verde para inicio y rojo para el final
- Comuertas (gateways) : los rombos con una X o + , indican decisiones o divisiones del flujo
