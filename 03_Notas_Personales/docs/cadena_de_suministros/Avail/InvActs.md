### InvActs.docx 

Describe los detalles de Inventarios reales. Se simulará no solo qué deberia pasar(bomb) sino qué esta pasando fisicamente en el almacen de AJE.

Que datos viajan en el paquete **InvActs** , segun los estandares de AJE .
1. Identificadores de ubicacion y producto: 
    - LocCd (Location Code) es el codigo de la planta o centro de distribucion (ej 8502)
    - ItemCd ( Item Code) es el codigo unico del producto o materia prima, es el nexo que une esta tabla con la de Boms

2. Datos y cantidad y estado
    - InvQty (Invetory Quanty) la cantidad fisica contada, es un valor decimal (ej 8040-0000)
    - AvailQty ;(Available Quantity) no siempre es igual a la anterior, representa lo que esta libre para usar
    - HoldQty (Hold Quantity) mercancia que esta en el almacen pero "bloqueado" por control de calidad o dañada.

3. Atributos de tiempo y registro (criticos para ETL) 
    - AsOfStamp (As of Date/time): la marca de tiempo exacta de cuando se tomo lectura en el ERP.Evita que el sistema use datos obsoletos

    - InvTm(inventory time) hora especifica del registro , necesaria para la precision en el motor AVAIl.

4. Metadatos de integracion 
    - Parcel Type(INVACTS) la etiqueta que le dice  ASW Glue, este paquete es de inventarios , no son nominas ni recetas
    - Iterface Table Name (IINVACTS) el nombre de la tabla puente, donde caeran los datos antes de entrar al postgres final.