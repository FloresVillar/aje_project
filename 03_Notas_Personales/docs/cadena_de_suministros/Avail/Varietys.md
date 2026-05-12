
### IVARIETYS.docx
Definición de Variedades (IVARIETYS)

Una variedad, o marca-sabor, es un atributo de un producto. El nombre corto de la variedad debe contener dos elementos, por ejemplo, la marca (**Brand**) y el sabor (**Flavor**).

####  Propiedades de la Interfaz (Properties)
* **Parcel Type**: VARIETYS
* **Interface Table Name**: IVARIETYS

####  Atributos Detallados (Required Attributes)
| Atributo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento `load_parcel` | |
| **VarietyCd** | Character(25) | Identificador alfanumérico único | 02 |
| **Variety** | Character(25) | Nombre corto único | B_Lem_Soda |
| **VarietyNm** | Character(100)| Nombre largo | Bill’s Lemon Soda |
| **VarietyTag1**| Character(64) | Tipo | CSD |
| **VarietySeq** | Character(25) | Secuencia de variedades en editores | 034 |

