import asyncio
import httpx
import random

API_URL = "http://127.0.0.1:8000/mediciones"

#se simulan 30 sensores distribuidos en las Yungas Jujeñas
SENSORES = [f"Sensor-Finca-Yungas-{i}" for i in range(1,31)]

async def enviar_telemetria_sensor(client: httpx.AsyncClient, sensor_id: str):
    payload = {
        "sensor_id": sensor_id,
        "temperatura": round(random.uniform(18.0, 33.0), 2),
        "humedad": random.randint(60, 95),
        "descripcion": "Lectura automática de telemetria de campo."
    }
    try:
        #Se envia la petición POST
        response = await client.post(API_URL, json=payload)
        print(f"[{sensor_id}] Status: {response.status_code} -> {response.json()}")
    except Exception as e:
        print(f"[{sensor_id}] Error de red: {e}")
        
async def main():
    print("Iniciando ataque de concurrencia: 30 sensores reportando al mismo milisegundo...")
    
    #Usando un unico cliente asíncrono para máxima velocidad
    async with httpx.AsyncClient() as client:
        #Se crean las 30 tareas concurrentes
        tareas = [enviar_telemetria_sensor(client, sensor) for sensor in SENSORES]
        #se ejecutan en paralelo completo
        await asyncio.gather(*tareas)
        
if __name__ == "__main__":
    asyncio.run(main())