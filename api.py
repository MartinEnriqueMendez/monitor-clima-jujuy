from fastapi import FastAPI, HTTPException
import sqlite3
from datetime import date

app = FastAPI(tittle="Monitor climático Agro - Jujuy")

def get_db_connection():
    #Conexión simple a la BD existente
    conn = sqlite3.connect("clima_agro.db")
    conn.row_factory = sqlite3.Row #Esto nos permite sacar datos por nombre de columna
    return conn

@app.get("/")
def home():
    return {"mensaje": "API de monitoreo climático de Jujuy activa"}

#Ruta para ver todo o filtrar por hoy
@app.get("/mediciones")
def leer_mediciones(hoy: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if hoy:
        fecha_actual = date.today().strftime("%Y-%m-%d")
        cursor.execute("SELECT * FROM mediciones WHERE date(fecha) = ? ORDER BY fecha DESC", (fecha_actual,))
    else:
        cursor.execute("SELECT * FROM mediciones ORDER BY fecha DESC LIMIT 20")
    
    filas = cursor.fetchall()
    conn.close()
    
    return [dict(f) for f in filas]
    
    #Nueva ruta para buscar una fecha específica (formato YYYY-MM-DD)
@app.get("/mediciones/fecha/{fecha_buscada}")
def buscar_por_fecha(fecha_buscada: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    #usar la función date() de SQLite para comparar solo la parte del dia
    cursor.execute("SELECT * FROM mediciones WHERE date(fecha) = ? ORDER BY fecha DESC", (fecha_buscada,))
    filas = cursor.fetchall()
    conn.close()
    
    if not filas:
        raise HTTPException(status_code=404, detail=f"No hay registros para la fecha {fecha_buscada}")
    
    return [dict(f) for f in filas]
    
