import requests
import time

time.sleep(12)

adjudicacion_compra = {
    "metodo": "registrarAdjudicacion",
    "contenido" : {"id_orden":"OC-550","proveedor":"AJE-PROV-01"}
}
print(f"[FULLSTEP] enviando adjudicacion a integrador...")
response = requests.post("http://wildfly_integrador_api:8080/ejecutaFuncion",json=adjudicacion_compra)