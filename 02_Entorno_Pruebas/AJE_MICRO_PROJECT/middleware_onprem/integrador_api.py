import requests
from flask import Flask,request,jsonify
# simulando el servidor wilffly/integrador
app = Flask(__name__)

ERP_URL = "http://as400_core:5001/services/InsertaOG"

@app.route('/ejecutaFuncion',methods=['POST'])
def integrador():
    datos_portal = request.json
    print(f"[INTEGRADOR] traduccion de json a xml para:{datos_portal['empleado']}")
    soap_xml = """\
     <soap:Envelope>\
        <id>{datos_portal['viaje_id']}</id> \
        <monto>{datos_portal['total']}</monto> \
    <soap:Envelope>"""  
    respuesta = requests.post("http://as400_core:5001/services/InsertaOG",data=soap_xml)
    return jsonify({"status":"Proceso en ERP","respuesta_soap":respuesta.text})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)