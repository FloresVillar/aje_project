
### MAKEBYSEGMENTS.docx

Este objeto técnico registra la programación de producción física por segmentos reportada al sistema.

#### Propiedades de la Interfaz (Properties)
* **Parcel Type**: MAKEBYSEGMENTS.
* **Interface Table Name**: XMAKESEGMENTS.

#### Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento `load_parcel`. | |
| **SegmentCD** | Character | Identificador único del segmento (MakeID – Segment). | `9999-1, 9999-2, etc.` |
| **Shift** | Character | Identificador del turno de producción. | `001, 002 or 003` |
| **Segment** | Number(10) | Identificador numérico del segmento. | `1, 2, 3, 4 . . . N` |
| **LocCd** | Character | Código de ubicación. | `92001` |
| **LineCd** | Character | Código de la línea de producción. | `7` |
| **ItemCd** | Character | Código del ítem. | `501316` |
| **RunFromTm** | DateTime | Fecha y hora de inicio programada. | `11/20/2020 2:19` |
| **RunThruTm** | DateTime | Fecha y hora de fin programada. | `11/21/2020 7:00` |
| **RunQty** | Number | Cantidad programada de la corrida. | `21903` |
| **RunHrs** | Number | Horas de producción estimadas. | `4.6` |
| **BoMVerCd** | Character | Código de versión de la lista de materiales. | `1` |
| **MakeId** | Number | Identificador único de corrida generado por el sistema. | `9999` |
