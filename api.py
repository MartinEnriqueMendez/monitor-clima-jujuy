from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import date
from pydantic import BaseModel
import redis
import json


app = FastAPI(title="Monitor climático Agro - Jujuy")

#2. Conectamos con el cliente de redis que está corriendo en Docker
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

class MedicionSensor(BaseModel):
    sensor_id: str
    temperatura: float
    humedad: int
    descripcion: str
    
#Configuración de CORS que ya habia
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect("clima_agro.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"mensaje": "API de monitoreo climático de Jujuy activa"}

@app.get("/mediciones")
def leer_mediciones(hoy: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()
    if hoy:
        fecha_actual = date.today().strftime("%Y-%m-%d")
        cursor.execute("SELECT * FROM mediciones WHERE date(fecha) = ? ORDER BY fecha DESC", (fecha_actual))
    else:
        cursor.execute("SELECT * FROM mediciones ORDER BY fecha DESC LIMIT 20")
    filas = cursor.fetchall()
    conn.close()
    return [dict(f) for f in filas]

@app.get("/mediciones/fecha/{fecha_buscada}")
def buscar_por_fecha(fecha_buscada: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mediciones WHERE date(fecha) = ? ORDER BY fecha DESC", (fecha_buscada,))
    filas = cursor.fetchall()
    conn.close()
    if not filas:
        raise HTTPException(status_code=404, detail=f"No hay registros para la fecha {fecha_buscada}")
    return [dict(f) for f in filas]

# --- Nueva ruta de recepción
@app.post("/mediciones")
def registrar_medicion(data: MedicionSensor):
    """
    Recibe la telemetria del sensor y la encola de inmediato en Redis,
    liberando la API al instante sin tocar la base de datos en forma directa.
    """
    try:
        #Estructuramos el payload que va a consumir el worker
        payload = {
            "temperatura": data.temperatura,
            "humedad": data.humedad,
            "descripcion": f"[{data.sensor_id}] {data.descripcion}"
        }
        
        #Encolar en Redis (Operacion en memoria: ultra veloz)
        r.lpush("cola_clima", json.dumps(payload))
        
        #Retornamos status 'enqueued'
        return {"status": "enqueued", "message": f"Medición de {data.sensor_id} recibida en caché."}
    
    except redis.RedisError as e:
        #Si redis se cae por alguna razón, devolvemos error de infraestructura
        raise HTTPException(status_code=500, detail=f"Error en el buffer de memoria Redis: {e}")
    