from pydantic import BaseModel, Field
from decimal import Decimal


class City(BaseModel):
    name_city: str

class Coordinate(BaseModel):
    geo_lat: Decimal = Field(max_digits=11, decimal_places=8, lt=180, gt=-180)
    geo_lon: Decimal = Field(max_digits=10, decimal_places=8, lt=90, gt=-90)

    
