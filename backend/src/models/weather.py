from pydantic import BaseModel
from typing import List


class City(BaseModel):
    name: str
    lat: float
    lon: float


class Weather(BaseModel):
    city: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    icon: str


class ForecastItem(BaseModel):
    date: str
    temperature: float
    description: str
    icon: str


class Forecast(BaseModel):
    city: str
    items: List[ForecastItem]
