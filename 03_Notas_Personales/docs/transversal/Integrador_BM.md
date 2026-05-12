# Documentación técnica integrador maestros.DOCX

## 1. Contenido del documento

### 2. CONSIDERACIONES PREVIAS (Pág. 3)
* **2.1. URLS** (Pág. 3)
* **2.2. Lista resumen de servicios proporcionados** (Pág. 3)

### 3. Uso de servicio registra base de datos (Pág. 4)
* **3.1. Descripción** (Pág. 4)
* **3.2. Cuerpo** (Pág. 4)
* **3.3. Respuesta** (Pág. 4)

### 4. Uso de servicio registra procedimiento almacenado (Pág. 6)
* **4.1. Descripción** (Pág. 6)
* **4.2. Cuerpo** (Pág. 6)
* **4.3. Respuesta** (Pág. 7)

### 5. Uso de servicio ejecutar función (Pág. 8)
* **5.1. Descripción** (Pág. 8)
* **5.2. Cuerpo** (Pág. 8)
* **5.3. Respuesta** (Pág. 9)

### 6. Demostración de uso (Pág. 10)


## 2. CONSIDERACIONES PREVIAS

### 2.1. URLS


| Ambiente | Url |
| :--- | :--- |
| Desarrollo | `http://10.101.8` |
| Producción | `http://10.101.8` |

### 2.2. Lista resumen de servicios proporcionados


| Nombre | Url | Método | Header Auth | Origen | Destino |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Registrar base de datos | `/registraDB` | POST | Bearer token | Big Magic | Big Magic |
| Registrar Procedimiento almacenado | `/registraSP` | POST | Bearer token | Big Magic | Big Magic |
| Ejecutar funcion | `/ejecutaFuncion` | POST | Bearer token | Big Magic | Big Magic |
