
### SHIPSCHD.docx 
Definición de Embarques Programados (SHIPSCHD)

Este objeto técnico registra la programación de embarques (Scheduled 
Shippers).

#### Propiedades de la Interfaz (Properties)
* **Parcel Type**: SHIPSCHD
* **Interface Table Name**: ISHIPSCHD

#### Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción / Columna | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento load_parcel | |
| **FrLocCd** | Character(25) | Identificador único del origen | 92001 |
| **ToLocCd** | Character(160) | Identificador único del destino | 92007 |
| **LoadTm** | DateTime | Hora de carga | 11/20/2020 02:38 |
| **DlvyTm** | DateTime | Hora de recepción | 11/21/2020 10:38 |
| **ItemCd** | Character(160) | Identificador único del ítem | 500248 |
| **ShipQty** | Float | Cantidad base | 5280 |
| **PalItemCd** | Character(160) | Código de pallet | 0001 |
| **PalQty** | Float | Cantidad de pallets | 24 |
| **ShipInvStatus** | Character(16) | Estados válidos: Schd, Load, Dlvd, Canc | Schd |
| **ShipCurrStatus** | Character(16) | Estados válidos: Schd, Load, Dlvd, Canc | Schd |
| **ShipType** | Character(16) | Tipos: Deploy, Cross-Deploy, Transfer, Buy, Purchase, Sale | Deploy |
| **LastExpStamp** | Date/Time | Sello de tiempo de última exportación | 11/21/2020 17:00 |
| **ShipHdrId** | Number(10) | Identificador de encabezado de embarque generado | 710952 |
| **LastImpStamp** | Date/Time | Sello de tiempo de última importación | 11/22/2020 07:00 |

