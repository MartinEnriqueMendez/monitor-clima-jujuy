import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY_NAME")
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather_data() -> dict:
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "temp": data['main']['temp'],
            "hum": data['main']['humidity'],
            "desc": data['weather'][0]['description']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None