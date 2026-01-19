import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5"
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0"
