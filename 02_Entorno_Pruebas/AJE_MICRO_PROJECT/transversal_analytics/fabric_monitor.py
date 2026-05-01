import pandas as pd
import time
import os
 
ITEMS_DB = "./database/items.csv"
INV_DB = "./database/invacts.csv"

def cargar_maestro_items():
    #carga de items
    if os.path.exists(ITEMS_DB):
        return pd.read_csv(ITEMS_DB,dtype={'ItemCd':str}).set_index('ItemCd').to_dict('index')
    return {}

AVAIL_DB = './database/avail_south_boms.csv'
def monitorear_eficiencia_boms(maestro):   
    print("\n[MONITOR] validando consistencia de recetas en AVAIL...")
    if os.path.exists(AVAIL_DB):
        df = pd.read_csv(AVAIL_DB)
        for _,fila in df.iterrows():
            item_id = str(fila['MakeItemCd'])
            nombre = maestro.get(item_id,{}).get('ItemNm','Producto Desconocido')
            familia = maestro.get(item_id,{}).get('ItemTag1','N/A')
            print(f"{nombre} (Cod:{item_id}) | Familia: {familia}")
            print(f">Producto: {fila['MakeItemCd']} | Receta Ver: {fila['BoMVerCd']}")
            print(f" Factor de Uso: {fila['UsePer']} | Desperdicio Permitido: {fila['WastePct']}%")
    else:
        print("[MONITOR] esperando a que AWS Glue sincronice datos...")

# este es el mmotor de AVAIL , no solo lee el stock , sino que cruza datos con el maestro de Items para dar nombres y pesos reales

INV_PATH = "./database/invacts.csv"
def auditar_inventario_logistico(maestro):
    if os.path.exists(INV_PATH):
        df_inv = pd.read_csv(INV_PATH)
        print("\n[FABRIC] auditoria de inventorios reales (IINVACTS)")
        for _,fila in df_inv.iterrows():
            item_id = str(fila['ItemCd' ])
            datos_item = maestro.get(item_id,{})
            nombre = datos_item.get('ItemNm','Desconocido')
            uom = datos_item.get('BaseUoM','UND')
            print(f">Parcel:{fila['parcelId']} | Planta:{fila['LocCd']} | SubLoc:{fila['SublocCd']}")
            print(f"Item: {nombre}({item_id})")
            print(f"Cantidad:{fila['InvQty']}{uom} | Fecha Toma: {fila['InvTm']}")
            print("-"*40)
    else:
        print("[FABRIC] Esperando sincronizacion de IINVACTS...")

def auditar_tablas():
    while True:
        print("[FABRIC]iniciando auditoria de tablas 'F'...")
        maestro = cargar_maestro_items()
        try:
            df = pd.read_csv('./database_legacy/mpersoef.csv')
            print(f"total empleados big_magic :{len(df)}",flush=True)
            monitorear_eficiencia_boms(maestro)
            auditar_inventario_logistico(maestro)
        except Exception as e:
            print(f"Error: {e}",flush=True)
        print("="*50)
        time.sleep(10)
    # cruzar las ordenes de gasto creadas


if __name__ == "__main__":
    auditar_tablas()