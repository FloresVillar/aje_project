from flask import Flask,request,jsonify
import pandas as pd


#simulando el core(big magic) y la base de datos
app = Flask(__name__)
#simulacion de la tabla "MPERSOEF" y "TCOALM1F"
db_erp = {
    "empleados": ["E123","E456"],
    "ordenes_gasto": []
}

@app.route('/services/InsertaOG/',methods=['POST'])
def web_services():
    # aqui se procesaria el cuerpo xml de un wsdl 
    data = request.data.decode('utf-8')
    print(f"[AS400] recibiendo XML SOAP: {data}")
    # simulando la insercion en Big Magic
    db_erp["ordenes_gasto"].append(data)
    return "<soap:Envelope> \
            <soap:Body>Exito</soap:Body> \
            </soap:Envelope>"

@app.route('/services/ActualizaPersonal',methods=['POST'])
def actualiza_personal():
    try:
        data = request.json
        CSV_PATH='./database/mpersoef_2.csv'
        df = pd.read_csv(CSV_PATH)
        nuevo_emp = pd.DataFrame([data])
        df = pd.concat([df,nuevo_emp],ignore_index=True)
        df.to_csv(CSV_PATH,index=False)
        print(f"[AS400] registro fisico actualizado MPERSOEF: {data['nombre']}")
        return jsonify({"resultado":"ACK","status":"Registro Grabado"}),200
    except Exception as e:
        return jsonify({"error" : f"falla comunicacion con core:{e}"}),502

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001)