### KINDS.docx
Definición de Kinds

Un **Kind**, o paquete de producto, es un atributo de un producto. El nombre corto del Kind debe contener tres elementos. Usando 15OZCN1/12 como ejemplo:

* **Size**– 15OZ
* **Container type** – CN
* **Packaging** – 1/12

#### Propiedades de la Interfaz (Properties)

* **Parcel Type**: KINDS
* **Interface Table Name**: IKINDS

#### Atributos Detallados (Required Attributes)

| Atributo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **parcelId** | Number(10) | ID de paquete recuperado del procedimiento load_parcel | |
| **KindCd** | Character(25) | Identificador alfanumérico único | 02 |
| **Kind** | Character(25) | Nombre corto único | 15OZ_CN1/12 |
| **KindNm** | Character(100) | Nombre largo | 15OZ CN 1/12 |
| **KindTag1** | Character(64) | Contenedor | CAN |
| **KindSeq** | Character(25) | Secuencia de Kinds en editores | |
| **IsProd** | Character(1) | Es un Producto | Y |
| **IsWIP** | Character(1) | Es un Trabajo en Progreso (ej. Jarabe) | |
| **IsMatl** | Character(1) | Es Materia Prima | |
| **IsPal** | Character(1) | Es un Pallet | |
| **IsReuse** | Character(1) | Es Reutilizable (ej. Shell) | |
| **Ismake** | Character(1) | Es Producido | Y |
| **IsBuy** | Character(1) | Es Comprado | |
| **IsRemake** | Character(1) | Es Reacondicionamiento o Multipack | |
| **IsSell** | Character(1) | Se Vende al Cliente | |
| **BaseUoM** | Character(12) | Unidad de medida para conteo de inventario | CASE, BIB |

---