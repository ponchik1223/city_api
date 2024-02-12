from sqlalchemy import Column,Integer, String
from sqlalchemy.types import DECIMAL


from src.database import Base


class CityModel(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, name='Город', unique=True)
    country = Column(String, nullable=False, name='Страна')
    latitude = Column(DECIMAL(precision=11, scale=8), name='Широта')
    longitude = Column(DECIMAL(precision=10, scale=8), name='Долгота')