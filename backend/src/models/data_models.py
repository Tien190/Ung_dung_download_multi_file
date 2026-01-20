from pydantic import BaseModel

class CityResult(BaseModel):
    name: str
    lat: float
    lon: float
