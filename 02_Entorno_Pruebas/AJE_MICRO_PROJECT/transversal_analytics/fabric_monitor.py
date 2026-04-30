import pandas as pd
import time
import os

def auditar_tablas():
    while True:
        print("[FABRIC]iniciando auditoria de tablas 'F'...")
        try:
            df = pd.read_csv('./database/mpersoef.csv')
            print(f"total empleados big_magic :{len(df)}",flush=True)
        except Exception as e:
            print(f"Error: {e}",flush=True)
        time.sleep(10)
    # cruzar las ordenes de gasto creadas

AVAIL_DB = './database/avail_south_boms.csv'
def monitorear_eficiencia_boms():
    print("\n[MONITOR] validando consistencia de recetas en AVAIL...")
    if os.path.existis(AVAIL_DB):
        df = pd.read_csv(AVAIL_DB)
        for _,fila in df.iterrows():
            print(f">Producto: {fila['MakeItemCd']} | Receta Ver: {fila['BoMVerCd']}")
            print(f" Factor de Uso: {fila['UsePer']} | Desperdicio Permitido: {fila['WastePct']}%")
    else:
        print("[MONITOR] esperando a que AWS Glue sincronice datos...")

if __name__ == "__main__":
    auditar_tablas()