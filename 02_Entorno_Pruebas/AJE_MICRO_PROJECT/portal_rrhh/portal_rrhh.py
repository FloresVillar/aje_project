import requests
import time

time.sleep(10)
# subproceso gestion contrato,al terminar dispara la persistencia al core legacy.
def ejecutar_gestion_de_contrato(id_emp,nombre,puesto,salario):
    url = "http://integrador_api:8080/bmp/evento_activacion"
    payload = {
        "id": id_emp,
        "nombre": nombre,
        "puesto" : puesto,
        "salario" : salario,
        "estado" : "ACTIVO"
    }
    try:
        response = requests.post(url,json=payload)
        print(f"[PORTAL] subproceso gestion de contrato finalizado para {nombre}")
        respuesta = response.json()['evento_fin']
        return respuesta
    except Exception as e:
        print(f"[RRHH] Error: {e}")

if __name__ == '__main__':
    #inicio proceso de diagrama
    ejecutar_gestion_de_contrato("E003","Trabajador","Arquitecto IT",3500)
    