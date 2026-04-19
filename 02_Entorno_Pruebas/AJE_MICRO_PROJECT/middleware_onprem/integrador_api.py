import requests
from flask import Flask,request,jsonify
import pandas as pd
import os

# simulando el servidor wilffly/integrador
app = Flask(__name__)

ERP_URL = "http://as400_core:5001/services/InsertaOG"

@app.route('/ejecutaFuncion',methods=['POST'])
def integrador():
    datos_portal = request.json
    print(f"[INTEGRADOR] traduccion de json a xml para:{datos_portal['empleado']}")
    soap_xml = f"""\
     <soap:Envelope>\
        <id>{datos_portal['viaje_id']}</id> \
        <monto>{datos_portal['total']}</monto> \
    <soap:Envelope>"""  
    respuesta = requests.post("http://as400_core:5001/services/InsertaOG",data=soap_xml)
    return jsonify({"status":"Proceso en ERP","respuesta_soap":respuesta.text})

#endpoint que representa la transicion al evento final del diagrama de administracion del personal

@app.route('/bmp/evento_activacion',methods=['POST'])
def handle_personal_activado():
    data = request.json
    print(f"[INTEGRADOR] reenviando evento de activacion a Core Legacy")
    url_core = "http://as400_core:5001/services/ActualizaPersonal"
    try:
        response = requests.post(url_core,json=data)
        return jsonify({"transaccion":"exitosa","evento_fin":"Personal_Activado","destino_db":"MPERSOEF","respuesta":response.text})
    except Exception as e:
        return jsonify({"error":f"falla comunicacion con core: {e}"}),502

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)