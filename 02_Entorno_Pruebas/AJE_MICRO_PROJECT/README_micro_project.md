# Emulacion del sistema big-magic , plan de viajes, portal de viajes, etc

1. Portal de viajes Envia la solicitud **solicitud_viaje** (un diccionario con claves viaje_id, empleado,total)al endpoint **http://integrador_api:8080/ejecutaFuncion** 

2. Integrador recibe el json desde **portal_viaje** , lo traduce a xml (SOAP) y envia **data=soap_xml** a **AS400**  al endpoint **http://as400_core:5001/services/InsertaOG**

3. En AS400 se agrega esa **data** que procede de integrador a **db_erp['ordenes_gasto']** y se  retorna el mensaje de exito en formato XML mediante SOAP(simulado)

4. De nuevo en integrador esa respuesta se encapsula dentro de un diccionario **{'status':..,'respuesta_soap':respuesta.text}**

5. Portal_viajes.py habia enviado la solicitud que inició el flujo en **respuesta = request.post(..,solicitud_viaje)** y se imprime la **respuesta**.

```bash
docker compose up --build


portal_viajes     | []PORTAL]Enviando solicitud a integrador...

portal_viajes     | respuesta final
portal_viajes     | {'respuesta_soap': '<soap:Envelope>             <soap:Body>Exito</soap:Body>             </soap:Envelope>', 'status': 'Proceso en ERP'}
fabric_monitor exited with code 0
portal_viajes exited with code 0
```

