import requests
#simula el fronted de Azure solicitando el gasto
solicitud_viaje = {
    "viaje_id" : "VIAJE_2026-MX",
    "empleado" : "E123",
    "total" : 500.00
}

print("[]PORTAL]Enviando solicitud a integrador...")
response = requests.post("http://integrador_api:8080/ejecutaFuncion",json=solicitud_viaje)
print("respuesta final")
print(response.json())