import pandas as pd
import time

def ejecutar_cierre_nomina():
    try:
        df = pd.read_csv('./database/mpersoef_2.csv')
        activos = df[df['estado']=='ACTIVO']
        total_nomina = activos['salario'].sum()
        print(f"[NOMINA] procesando para {len(activos)} empleados")
        for i,fila in activos.iterrows():
            print(f" > Dispersion Bancario: {fila['nombre']} | Monto: ${fila['salario']}")
        print(f"[NOMINA] cierre exitoso. Total dispersado : ${total_nomina}")
        print(f"[NOMINA] generando reportes fiscales y metricas")
    except Exception as e:
        print(f"[NOMINA] error en el proceso:{e}")

#lee los cambios realizados por el proceso de administracion
def subproceso_captura_novedades():
        print("\n [BPMN] ejecutando captura novedades..",flush=True)
        df = pd.read_csv('./database/mpersoef_2.csv')
        novedades = df[df['estado']=='ACTIVO']
        return novedades

def subproceso_calculo_liquidacion(datos):
    print(f"calculo y liquidacion {len(datos)} registros",flush=True)
    total = datos['salario'].sum()
    return total

if __name__ == '__main__':
    while True:
        #ejecutar_cierre_nomina()
        nomina_data = subproceso_captura_novedades()
        total_pago = subproceso_calculo_liquidacion(nomina_data)
        print(f"[BPMN] evento fin: pago realizado, total: ${total_pago}",flush=True)
        time.sleep(60) # procesamientoo de nomina via Cron jobs cada cierto tiempo
        