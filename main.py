from weather_api import get_weather_data
from database import init_db, save_measurement

def run():
    print("Iniciando monitoreo climático...")
    init_db()
    
    data = get_weather_data()
    if data:
        save_measurement(data['temp'], data['hum'], data['desc'])
        print(f"Éxito: {data['temp']}° C registrados para {data['desc']}.")
    else:
        print("No se pudo obtener los datos.")
        
if __name__ == "__main__":
    run()