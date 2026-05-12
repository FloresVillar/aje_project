### MAKEACTS-Segments.docx

Este objeto técnico registra los segmentos de ejecución de producción física reportados desde las líneas.

####  Propiedades de la Interfaz (Properties)
* **Parcel Type**: MAKEACTS.
* **Interface Table Name**: IMAKEACTS.

#### Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento `load_parcel`. | |
| **SegmentCD** | Character | Identificador único del segmento de producción (MakeID – Segment). | `9999-1` |
| **Shift** | Character | Identificador del turno de producción. | `001, 002 o 003` |
| **LineCd** | Character(25) | Identificador único de la línea de producción. | `THAI_PL-2` |
| **MakeItemCd** | Character(25) | Identificador único del ítem producido. | `501068` |
| **BOMverCd** | Character(25) | Identificador único de la lista de materiales (BOM). | `92001` |
| **RunFromTm** | DateTime | Fecha y hora de inicio de la corrida. | `11/20/2020 02:19` |
| **RunThruTm** | DateTime | Fecha y hora de fin de la corrida. | `11/21/2020 10:38` |
| **RunNetQty** | Float | Cantidad neta producida. | `21903` |
| **RunHrs** | Float | Horas totales de producción. | `32.32` |
| **AsOfStamp** | DateTime | Fecha y hora en que se registró el valor. | `11/21/2020 17:05` |
| **MakeInvStatus**| Character(16) | Estado de la corrida al momento del inventario. | `Scheduled, Running, Delivered, Cancelled` |
| **MakeCurrStatus**| Character(16) | Estado actual de la corrida de producción. | `Scheduled, Running, Delivered, Cancelled` |
| **RunGrossQty**| Float | Cantidad bruta total producida. | `21950` |
