import requests
from flask import Flask,request,jsonify
import pandas as pd
import os
import time
import threading 

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
# para boms
DESTINO_AVAIL  = "./database/avail_south_boms.csv"        #simula el RDS Postgres A10_SOuTH
@app.route('/aws_glue/ETLBomsJob-Corp',methods = ['POST'])
def run_etl_boms():
    print("[GLUE- JOB] iniciando ETLIbomsJob-Corp...")
    try:
        res = requests.get('http://as400_core:5001/services/GetBOMs')
        datos_raw = res.json()                                          # extraccion de big Magic/AS400
        print (f"[GLUE] transformando {len(datos_raw)} resgistros de recetas")   # transformacion (normalizacion) aplicar redondeo o limpieza
        df_final = pd.DataFrame(datos_raw)
        df_final.to_csv(DESTINO_AVAIL,index = False )     #carga hacia AVAIL en AWS
        return jsonify({"status":"EXITO","records_processed":len(datos_raw)})
    except Exception as e:
        return jsonify({"status":"ERROR","detail":str(e)}),500
#simula AWS EventBringe disparando el job cada cierto tiempo
def disparador_aws_glue():
    time.sleep(15)
    while True:
        try:
            print(f"[EVENTBRINGE] Es hora de sincronizar AVAIL...")
            requests.post("http://127.0.0.1:8080/aws_glue/ETLBomsJob-Corp")
        except Exception as e:
            print(f"[ERROR] disparador fallido : {e}")
        time.sleep(40)
#este modulo(middleware_onprem) simula el Job de AWS Glue(ETLItems-Corp). Su funcion es succionar el paquete de satelite y despositarlo en el volumen compartido database/
DATABASE_PATH = "database/items.csv"
@app.route('/aws_glue/ETLItemsJob-Corp',methods=['POST'])
def run_items_etl():
    response = requests.get("htpp://as400_core:5001/services/GetItems") # 1. extrae desde el satelite
    data = response.json()
    df = pd.DataFrame(data)                         #  2. transformacion
    df['BaseWt'] = pd.to_numeric(df['BaseWt'])      #   validacion de integridad(que los pesos sean numericos)
    os.makedirs('database',exist_ok=True)           # 3  carga al volumen compartido (simulando RDS Postgres)
    df.to_csv(DATABASE_PATH,index=False)    
    return jsonify({"status":"succes","records_processed":len(df)})


if __name__=='__main__':
    threading.Thread(target=disparador_aws_glue,daemon=True).start()
    app.run(host='0.0.0.0',port=8080)