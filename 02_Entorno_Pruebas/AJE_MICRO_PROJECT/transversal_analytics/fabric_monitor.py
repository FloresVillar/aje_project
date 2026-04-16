import pandas as pd
import time

def auditar_tablas():
    while True:
        print("[FABRIC]iniciando auditoria de tablas 'F'...")
        try:
            df = pd.read_csv('./database/mpersoef.csv')
            print(f"total empleados big_magic :{len(df)}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(10)
    # cruzar las ordenes de gasto creadas
if __name__ == "__main__":
    auditar_tablas()