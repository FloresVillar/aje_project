#### WS BM - Efletex(Anuncios Regulares).docx


```bash
COMPROBAR STATUS DE ENVIO
Url: status-envio
Método: HTTP REQUEST | GET

Parámetros
Tipo de dato
Datos
tokenapi
string
proporcionado por Efletex
clienteid
int
id del cliente en Efletex
fecha
date
formato yyyy-mm-dd


{
"data": [
{
"envioid": 1598, "status": "RESERVADO",
"clienteid": 626,
"transportistaid": 214, "transportista_codigo": "", "fecha": "2017-08-04 12:04:27",
"precio": "900",
"carga_desde": "2017-08-14", "carga_hasta": null, "entrega_desde": "2017-08-15", "entrega_hasta": null
}, {
"envioid": 1599, "status": "EXPIRADO", "clienteid": 626, "transportistaid": "",
"transportista_codigo": "", "fecha": ""
},

],
"status": "success", "results": 1,
"message": "Lista de envios con status reservado y eliminado"
}







PUBLICAR ENVIO


Descripción: este servicio se utiliza para crear el registro con los datos del envío, para después ser procesado en Efletex. Debe enviarse la información del o los pedidos que conforman este envío (los datos del cliente, los litros y pesos (kg) de los pedidos).

URL: apiV2/envios
METODO: POST


Parametros:
Tipo Dato
Datos
tokenapi
string
proporcionado por efletex
clienteid
int
id del cliente en efletex
codigo_envio
string
id del envio en el ERP
fecha_carga_desde
date
formato yyyy-mm-dd
fecha_carga_hasta
date
formato yyyy-mm-dd
fecha_entrega_desde
date
formato yyyy-mm-dd
fecha_entrega_hasta
date
formato yyyy-mm-dd
hora_carga_desde
time
formato hh:mm:ss
hora_carga_hasta
time
formato hh:mm:ss
hora_carga_desde
time
formato hh:mm:ss
hora_carga_hasta
time
formato hh:mm:ss
fecha_expiracion
date
formato yyyy-mm-dd
hora_expiracion
time
formato hh:mm:ss
estado_carga
ciudad_carga direccion_carga ubicacion_carga contacto_carga telefono_carga lugar_carga otro_lugar_carga estado_entrega ciudad_entrega direccion_entrega ubicacion_entrega contacto_entrega telefono_entrega lugar_entrega
otro_lugar_entrega
int
string string coords string numeric int string int string string coords string string int
string
id del estado/depto.
formato latitud,longitud id de lugares efletex
id del estado/depto..
formato latitud,longitud id de lugares efletex




artículos
array
contiene artículos en formato json
titulo
string


tipo_precio
int
1=fijo,2=libre,3=mixto
tipo_envio
int
0=publico,1=privado
grupoid
int
id del grupo del cliente efletex
servicioid
int
id del servicio efletex
tipovehiculoid
int
id del tipo de vehículo efletex
metodopagoid
int
id del método de pago efletex
precio_envio
float


porcentaje_inicial
float
mayor a 0 menor a 100
condiciones_pago
string


transportistas
array
códigos de transportistas
elevador_carga
int
0=false,1=true
cargar_interior
int
0=false,1=true
llamar_antes_entrega
int
0=false,1=true
elevador_entrega
int
0=false,1=true
entrega_interior
int
0=false,1=true
proteccion_frio
int
0=false,1=true
clasificar_separar
int
0=false,1=true
persona_invidente
int
0=false,1=true
solo_comunidad
int
0=false,1=true
mostrar_ofertantes
int
0=false,1=true
codigo_cliente_erp
string
código del cliente en el erp
nombre_cliente
string


razon_social_cliente
string


canal_cliente
string


codigo_pedido
array
info de pedidos
fecha_erp
date
formato yyyy-mm-dd hh:ii:ss





Parámetro: transportistas
Tipo: array
Contiene los códigos de los transportistas separados por comas. Previamente deben estar relacionados con el cliente.
transportistas = codigo1,codigo2,cod….;

Parámetro: artículos
Tipo: array
Contiene datos json de los artículos a publicar. articulos =
{“unidadid”:””,”peso”:””,”unidad_peso”:””,”cantidad”:””,”largo”:””,”alto”:””,”ancho”:””,”unidad_ medida”:””,”descripcion”:””,”apilable”:””,”peligroso”:””,”perecedero”:””}


Atributos
Tipo de Dato
Datos
unidadid
int
id de la unidad en efletex
peso
float


unidad_peso
string
cadenas permitidas Kg, Lb, Tn
cantidad
int
numero de unidades
largo
float
dimensión articulo
alto
float
dimensión articulo
ancho
float
dimensión articulo
unidad_medida
string
cadenas permitidas cm,m,in
descripcion
string


apilable
int
0=false,1=true
peligroso
int
0=false,1=true
perecedero
int
0=false,1=true



Parámetro: codigo_pedido
Tipo: array
Contiene datos json de los pedidos que conforman el anuncio codigo_pedido = {“codigo”:””,”litros”:””,”peso”:””,”fecha”:””,”hora”:””}

Atributos
Tipo de Dato
Datos
codigo
string
codigo del pedido
litros
float
total de litros del pedido
peso
float
total de kg del pedido
fecha
date
formato yyyy-mm-dd
hora
time
formato hh:ii:ss



Consideraciones
otro_lugar_carga es obligatorio si lugar_carga=6 otro_lugar_entrega es obligatorio si lugar_entrega=6 grupoid es obligatorio si tipo_envio=1
transportistas es obligatorio si desea hacer envios dirigidos.
metodopagoid, tipovehiculoid, servicioid, condicionespago pueden ir vacíos si no va a definirlos en el envío.


Ejemplo de llamada:
https://efletex.com/apiV2/envios?tokenapi=valor-token&clienteid=idcliente-proporcionado&codigo_envio=12345&fecha_carga_desde=2019-05-14&fecha_carga_hasta=2019-05-14&fecha_entrega_desde=2019-05-16&fecha_entrega_hasta=2019-05-16&hora_carga_desde=13:00:00&hora_carga_hasta=23:00:00&hora_entrega_desde=07:00:00&h ora_entrega_hasta=16:00:00&fecha_expiracion=2019-05-14&hora_expiracion=12:30:00&estado_carga=2431&ciudad_carga= TUXTLA GUTIERREZ&direccion_carga=LA SALLE 323 &ubicacion_carga= 16.7401171,-93.0926997&contacto_carga=SUPERVISOR DE TRANSPORTE&telefono_carga=9611234567&lugar_carga=2&estado_entrega=2431&ciudad_entre ga= TUXTLA GUTIERREZ&direccion_entrega=5 de mayo &ubicacion_entrega= 16.752341, - 93.106323&contacto_entrega=CLIENTE&telefono_entrega=9611234567&lugar_entrega=2&articul os=[{"unidadid":"29","peso":"30","unidad_peso":"Tn","cantidad":"1","largo":"13.5","alto":"2.6","a ncho":"3.6","unidad_medida":"m","descripcion":"documentos vigentes de la unidad","apilable":"0","peligroso":"0","perecedero":"0"}]&titulo=VIAJE TUXTLA – 5 DE MAYO &tipo_precio=1&tipo_envio=1&grupoid=23&servicioid=1&tipovehiculoid=8&metodopagoid=2&pr ecio_envio=3840&porcentaje_inicial=0&condiciones_pago=PAGO 15 DIAS DESPUES DE ENTREGADA LA
FACTURA&elevador_carga=0&cargar_interior=0&llamar_antes_entrega=0&elevador_entrega=0& entrega_interior=0&proteccion_frio=0&clasificar_separar=0&persona_invidente=0&solo_comunid ad=1&mostrar_ofertantes=0&transportista=[]&codigo_pedido=[{"codigo":"OC324","litros":23456, "peso":23456,"fecha":"2019-07-20","hora":"11:00:00"}]&codigo_cliente_erp=04567&nombre_cliente=TEST&canal_cliente=TESTIN G&razon_social_cliente=TEST EFLETEX&fecha_erp=2019-06-15 14:06:40

Ejemplo de respuesta satisfactoria:

{
"data": { "envioid": null,
"status": "PENDIENTE DE PUBLICAR"
},
"status": "success",
"results": "1",
"message": "Datos Recibidos"
}

Ejemplo de respuesta de error:

{
"status": "error",
"results": "0",
"message": "mensaje de error"
}




DOCUMENTACION ENVIO
Descripción: se envían los datos de las guías de remisión, con la información general del cliente y transportista.

URL: apiV2/documentacion-envio
Metodo: POST
Envío de datos por body


Parametros:
Tipo Dato
Datos
tokenapi
string
proporcionado por efletex
data
array
array con estructura json


Parametros de la estructura data


Campo
Tipo Dato
Datos
envioid
int
id del envio (ref Efletex)
clienteid
int
id del cliente de Efletex
tipo_documento
string
OC=Orden Carga, G= Guia
folio_orden_carga
string
seriado de la orden de carga
codigoFlete
string
codigo del envio en el ERP
fecha_orden_carga
date time
formato yyyy-mm-dd hh:ii:ss
status_orden_carga
string
liquidada o no liquidada, cancelada
folio_guia
string
seriado de la guía
fecha_guia
date time
formato yyyy-mm-dd hh:ii:ss
litros
float
total de litros de la guía
peso
float
total de kg de la guía
status_guia
string
liquidada o no liquidada, cancelada
tipo_vehiculo
string
codigo + descripción (cod,descr)
codigo_cliente
string
codigo del cliente en el ERP
salida_guia
string
procedimiento de la guía
codigo_transportista
string
codigo del trt en el ERP
placa
string
placa del vehiculo
chofer
string
codigo del conductor en el ERP
tarimas
string
numero de palets
calle_entrega
string
calle del punto de entrega
ciudad_entrega
string
ciudad del punto de entrega
estado_entrega
string
estado del punto de entrega
capacidad_codigo
string
codigo de la capacidad del vehiculo
capacidad_nombre

Ejemplo llamada
string
descripción de la capacidad


{"tokenapi":"token-proporcionado","data":[{"fecha_orden_carga":"2019-07-09 09:32:15","codigoFlete":"00300001FLT0000010311","tipo_documento":"OC","status_orden_carga ":"ACTIVO","envioid":"12345","clienteid":idproporcionado,"folio_orden_carga":"GRA 0000572227"}]}


{"tokenapi":" token-proporcionado ","data":[{"codigoFlete":"00300001FLT0000010311","estado_entrega":"TABASCO ","chofer":1702435,"capacidad_nombre":"SENCILLO	","codigo_cliente": idproporcionado,"tarimas":22,"envioid":"12345","folio_orden_carga":"GRA 0000572227","calle_entrega":"ANACLETO CANABAL 1A
SECCION","ciudad_entrega":"CENTRO","litros":21348.54,"peso":16317.171999999999,"status_gui a":"ACTIVO","tipo_vehiculo":"003,TRAILER","tipo_documento":"G","folio_guia":"HP-0000000000229475","fecha_guia":"2019-07-09
12:25:30.063","precinto":"0136344","codigo_transportista":1589779,"capacidad_codigo":"001"," placa":"52AF1B ","clienteid":1495,"salida_guia":"EMPRESA "}]}




Ejemplo respuesta satisfactoria:
{
"status": "success", "errors": "array-errores",
"inserts": "numero-insertados", "message": "Consumo Exitoso"
}


Ejemplo error:
{
"status": "error", "errors": "array-errores",
"inserts": "numero-insertados",
"message": "Ocurrio un error en el WS documentacionEnvio, code 1"
}




```




