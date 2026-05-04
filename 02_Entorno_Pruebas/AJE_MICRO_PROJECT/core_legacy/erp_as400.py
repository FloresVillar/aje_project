from flask import Flask,request,jsonify
import pandas as pd
import os
#es BD magic mx test (aws cloud)
#simulando el core(big magic) y la base de datos
app = Flask(__name__)
#simulacion de la tabla "MPERSOEF" y "TCOALM1F"
db_erp = {
    "empleados": ["E123","E456"],
    "ordenes_gasto": [],
    "compras_fullstep" : []
}

# simula al servidor BIG MAGIC MXTEST SRVGLZADB01
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

# --capa de datos -- (SPs de salesForce/Efletex)
def sp_registrar_compra_aje(id_pedido,monto):
    print(f"[DB MAGIC ] logica interna {id_pedido}")
    db_erp["compras_fullstep"].append({"id":id_pedido,"monto":monto})
    return "OK"

# --capa de red -- (ENDPOINT de los wsdls)
@app.route('/services/ComprasAjeGroupWSBinding',methods=['POST'])
def compras_binding():
    data = request.data.decode('utf-8')
    resultado = sp_registrar_compra_aje("FS-101",500.0)
    return f"<soap:Envelope>\
                <soap:Body>Exito FullStep:{resultado}</soap:Body>\
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

BOM_PATH = './database/iboms.csv'
if not os.path.exists('./database/iboms.csv'):
    df_boms = pd.DataFrame(columns = ['MakeItemCd','BoMVerCd','UseItemCd','UsePer','WastePct'])
    df_boms.loc[0] = ['501068','92001','MAT-PRIMA-01',0.33005537,2.5] # registro de ejemplo, producto 501068 usa 0.33 de jarabe
    df_boms.to_csv(BOM_PATH,index=False)

#cuando los jobs como ETLItemJob-Corp hacen request a /services/GetItems .. simula a SQL DMRRHHMXTEST(on-premise)
@app.route('/services/GetBOMs',methods = ['GET'])
def get_boms():
    df = pd.read_csv('./database/iboms.csv')
    return jsonify(df.to_dict(orient = 'records'))

# este endpoint entrega el paquete completo de datos , incluyendo identificadores de parcela  sub-localizacion
@app.route('/services/GetInventory',methods=['GET'])
def get_inventory():
    inventory_db = [
        {
            "parcelId": 5501,          # Number(10) - ID retornado por load_parcel
            "LocCd": "8502",           # Character(25) - Location unique identifier
            "ItemCd": "501068",        # Character(25) - Item unique identifier
            "InvTm": "11/20/2020 02:19", # DateTime - Date/Time count is made
            "AsOfStamp": "11/20/2020 02:19", # DateTime - Date/Time value was recorded
            "InvQty": 8040.0,          # Float - Count in Base UOM
            "SublocCd": "01" 
        }
    ]
    return jsonify(inventory_db)

# recordar, este modulo(core_legacy) actua como el satelite original(servidor SRVGLZADB01) que expone la tabl de interfaz IITEMS
@app.route('/services/GetItems',methods=['GET'])
def get_items():
    items_db = [
        {
            "parcelId": 1001,
            "ItemCd": "501068",
            "Item": "15OZ_CN1/12_DTSODA",
            "ItemNm": "BIG COLA 3L",
            "KindCd": "02",      # Gaseosas
            "VarietyCd": "16",   # Cola
            "Variant": "Standard",
            "ItemTag1": "CSD",   # Familia: Carbonated Soft Drinks
            "IsProd": "Y", "IsWIP": "N", "IsMatl": "N", "IsPal": "N",
            "IsBuy": "N", "IsSell": "Y",
            "BaseUoM": "CASE",
            "BaseWt": 18.50,     # Peso por caja
            "ShipWt": 1350.0     # Peso por Pallet (estándar AJE)
        },
        {
            "ItemCd": "100045",
            "ItemNm": "AZUCAR INDUSTRIAL",
            "KindCd": "05", "ItemTag1": "RAW",
            "IsProd": "N", "IsMatl": "Y", "IsBuy": "Y", "IsSell": "N",
            "BaseUoM": "KG", "BaseWt": 1.0, "ShipWt": 1000.0
        }
    ]
    return jsonify(items_db)



if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001)