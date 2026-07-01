import redis
import sqlite3
import json
import time

print("Worker de streaming de agro listo y escuchando la cola...")

#1 Nos conectamos con el redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def guardar_en_sqlite(temperatura, humedad, descripcion):
    """Logica tradicional para persistir en la base de datos local"""
    conn = sqlite3.connect("clima_agro.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mediciones (temperatura, humedad, descripcion) VALUES (?,?,?)",
        (temperatura, humedad, descripcion)
    )
    conn.commit()
    conn.close()
    

#2.Bucle de procesamiento (polling)
while True:
    try:
        #BRPOP es un comando que espera de forma bloqueante hasta que aparezca
        #un elemento en 'cola_clima'. Si no hay nada, no consume CPU.
        #el 0 significa que espera inmediatamente.
        resultado = r.brpop("cola_clima", timeout=5)
        
        if resultado is None:
            continue #Vuelve al inicio del bucle al escuchar,
        
        nombre_cola, datos_json = resultado 
        
        #Parseamos el JSON que metió la API
        medicion = json.loads(datos_json)
        
        print(f"[Worker] Procesando del buffer: {medicion['descripcion']} -> Temp: {medicion['temperatura']}°C")
        
        #Guardar en la BD de forma segura e individual
        guardar_en_sqlite(
            medicion['temperatura'],
            medicion['humedad'],
            medicion['descripcion']
        )
        
    except redis.RedisError as re:
        print(f"Error de conexión de redis: {re}")
        time.sleep(5) #Se espera antes de reintentar
    except Exception as e:
        print(f"Error inesperado en el procesamiento: {e}")

