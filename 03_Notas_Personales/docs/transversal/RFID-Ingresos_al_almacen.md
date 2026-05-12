# FLUJO AUTOMATIZADO DE TRASLADO DE TARIMAS: RFID & ERP BIG MAGIC

Este flujo describe la transición tecnológica de una tarima desde su etiquetado en producción hasta su ingreso sistémico en el almacén de producto terminado. El sistema utiliza hardware RFID y el software DataLogger para alimentar automáticamente el ERP Big Magic, eliminando registros manuales.

---

### Esquema de Identificación y Procesamiento

```text
[ IDENTIFICACIÓN Y CAPTURA DE DATOS ]       [ PROCESAMIENTO Y EJECUCIÓN EN ERP ]
+-------------------------+                 +----------------------------+

| Vinculación de          |                 | [MXBDAJE]                  |
| Identidad Digital       |                 | USP_CODBAR_LECTURA_RFID    |
| (Etiqueta térmica +     |                 | (Stored Procedure)         |
| copia código a RFID)    |                 +-------------+--------------+
+------------+------------+                               |

             |                                            v
             v                              +----------------------------+
+-------------------------+       SP        | Sincronización             |
| Lectura Automatizada    | <-------------> | con Big Magic              |
| DataLogger (Antenas     | [RFID]          | (Transferencia de lectura) |
| fijas al salir de Prod) | USP_GENERA_INP  +-------------+--------------+
+-------------------------+                               |
                                                          v
                                            +----------------------------+

                                            | Ejecución de               |
                                            | Procesos en Paralelo       |
                                            | (Crea INP y actualiza OP)  |
                                            | [MXBDAJE]                  |
                                            | USP_ETIQ_RECEP_RFID        |
                                            +----------------------------+
```

---

### Secuencia RFID (Diagrama de Proceso)

```text
+---------------------------------------+      STORES PROCEDURES / JOBS

| Genera e Imprime Etiqueta Térmica     | -->  MXBDAJE.USP_ETIQUETA
|                                       |      BDRFID.USP_ACTUALIZA_SENSOR
+-------------------+-------------------+

                    |
                    v
+---------------------------------------+
| Copia de Código de Barras a chip      |
+-------------------+-------------------+

                    |
                    v
+---------------------------------------+
| Lectura RFID                          | -->  JOB: BDRFID.USP_GENERA_INP
|                                       |      SP:  MXBDAJE.DBO.USP_CODBAR_LECTURA_RFID
+-------------------+-------------------+

                    |
                    v
+---------------------------------------+
| Ingreso al almacen de PT              | -->  SP:  MXBDAJE.USP_ETIQ_RECEP_RFID
| (creacion de INP)                     |
+---------------------------------------+
```

---

### Detalle de Secuencia y Parámetros


| Etapa | Tipo | Stored Procedure / Proceso | Base de Datos | Parámetros Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Genera e Imprime Etiqueta** | SP | `MXBDAJE.USP_ETIQUETA` | MXBDAJE | LSLN10MAGIC,58162 |
| | SP | `BDRFID.USP_ACTUALIZA_SENSOR` | BDRFID | LSLN10MAGIC,58162 |
| **Copia de Código a chip** | - | (Vinculación Digital) | - | - |
| **Lectura RFID** | JOB | `BDRFID.USP_GENERA_INP` | BDRFID | - |
| | SP | `MXBDAJE.USP_CODBAR_LECTURA_RFID` | MXBDAJE | - |
| **Ingreso al almacén** | SP | `MXBDAJE.USP_ETIQ_RECEP_RFID` | MXBDAJE | - |
