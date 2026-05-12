### SHIPACTS.docx

Este objeto técnico registra la información de embarques reales (Actual Shippers).

####  Propiedades de la Interfaz (Properties)
* **Parcel Type**: SHIPACTS
* **Interface Table Name**: ISHIPACTS

####  Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento load_parcel | |
| **ShipHdrId** | Number(10) | ID generado para el encabezado de factura/transacción de embarque | 10000345 |
| **FrLocCd** | Character(25) | Identificador único del origen | 92001 |
| **ToLocCd** | Character(25) | Identificador único del destino | 92007 |
| **LoadTm** | DateTime | Hora de carga | 11/20/2020 02:38 |
| **DepartTm** | DateTime | Hora de salida de la ubicación de origen | 11/20/2020 03:00 |
| **DlvyTm** | DateTime | Hora de entrega/recepción | 11/21/2020 10:38 |
| **ItemCd** | Character(25) | Identificador único del ítem | 500248 |
| **LoadQty** | Float | Cantidad cargada | 5280 |
| **RcvdQty** | Float | Cantidad recibida | 5280 |
| **ShipInvStatus** | Character(16) | Estado de la carga al momento del inventario | Schd, Load, Rcvd, Canc |
| **ShipCurrStatus** | Character(16) | Estado actual de la carga | Schd, Load, Rcvd, Canc |
| **InvLotId** | Number(10) | ID generado para un lote de corrida de producción | 193059 |

