### Items.docx
**Un producto es una combinacion de tipo , variedad y opcionalmente variante**. El nombre corto del producto debe contener dos elementos ej : 15OZ_CN1/12_BSTDTSODA 

- tipo      :   15OZ_CN1/12
- variedad  :   BSTDTSODA

1. **Identidad y clasificacion**: Estos campos perrmiten que el sistema AVAIL agrupe los productos para reportes gerenciales 
    - **ItemCd & ItemNm** : el codigo alfanumerico (ej 13439) y el nombre largo descriptivo (150Z CN 1/12 DTSODA)
    - **KindCd & VarietyCd** : clasificacion tecnica . El kind define la naturaleza (ej Gaseosa) y Variety (el sabor o tipo especifico)
    - itemTag1 (familia): Etiqueta de agrupacion superior como **CSD(carbonated soft drinks)**
    - Variant : Atributo para distinguir versiones de un mismo producto, como una edicion de exportacion.
2. **Flags de estados** (las reglas del negocio): Estas son caracteres de un solo digito (Y/N) que le dicen al integrador como tratar el dato
    - IsProd (Is Produced) : indica si el item sale de un linea de produccio nde AJE 
    - IsMatl (is material) : Indica si es materi prima (aucar, preformas, etiquetas)
    - IsWIP (Work in progress) : para productos intermedios , como el jarabe (Syrup) que aun no ha sido embotellado.
    - IsPal ( Is Pallet) : Define si el item es una unidad de transporte (pallet)
    - IsBusy & IsSell : Determinan si el item se compra a proveedores o se vende directamente a cliente.
3. **Atributos fiscicos y logisticos** (La inteligencia de carga) Cruciales para que el fabric_monitor calcule pesos y volumenes de despacho.
    - **BaseUoM** (base unit of measure) la unidad minima de inventario , por ejemplo, CASE (caja) o BIB (bag-in-box)
    - **BaseWt** (Base Weight) el peso de la unidad (ej 6.37) es vital para no sobrecargar los camiones en la simulacion de despacho
    - **ShipWt** (Ship Weight) El peso total cuando se envia en unidades mayores, como un pallet completo (ej 1350)
