from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.services.weather_service import (
    search_city,
    get_current_weather,
    get_forecast
)

app = FastAPI(title="Weather App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Weather API is running"}


@app.get("/cities")
def autocomplete_city(q: str = Query(..., min_length=2)):
    return search_city(q)


@app.get("/weather")
def weather(lat: float, lon: float):
    return get_current_weather(lat, lon)


@app.get("/forecast")
def forecast(lat: float, lon: float):
    return get_forecast(lat, lon)
