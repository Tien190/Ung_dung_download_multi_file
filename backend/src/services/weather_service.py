import requests
from src.config import (
    OPENWEATHER_API_KEY,
    BASE_WEATHER_URL,
    GEOCODING_URL
)


def search_city(city_name: str):
    url = f"{GEOCODING_URL}/direct"
    params = {
        "q": city_name,
        "limit": 5,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return [
        {
            "name": f"{c['name']}, {c.get('country')}",
            "lat": c["lat"],
            "lon": c["lon"]
        }
        for c in response.json()
    ]


def get_current_weather(lat: float, lon: float):
    url = f"{BASE_WEATHER_URL}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "vi",
        "appid": OPENWEATHER_API_KEY
    }

    data = requests.get(url, params=params).json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }


def get_forecast(lat: float, lon: float):
    url = f"{BASE_WEATHER_URL}/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "vi",
        "appid": OPENWEATHER_API_KEY
    }

    data = requests.get(url, params=params).json()

    items = []
    for item in data["list"][::8]:  # mỗi ngày 1 mốc
        items.append({
            "date": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"]
        })

    return {
        "city": data["city"]["name"],
        "items": items
    }
