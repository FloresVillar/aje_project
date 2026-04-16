from flask import Flask,request
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

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001)