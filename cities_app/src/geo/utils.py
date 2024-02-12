from fastapi import status
from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from aiohttp import ClientSession
from decimal import Decimal


from src.config import API_KEY
from .models import CityModel
from .schemas import Coordinate


async def fetch(session: ClientSession, name: str) -> dict:
    '''получает данные о городе через API https://yandex.ru/dev/geocode/doc/ru/response'''
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={name}&format=json'
    
    async with session.get(url) as response:
        data = await response.json()
        
    return data

async def get_json_data(name: str) -> dict:
    '''парсер json для получение корректного названия города, страны, широты и долготы'''
    async with ClientSession() as client_session:
        data = await fetch(client_session, name)

    GeoObject: dict = data['response']['GeoObjectCollection']['featureMember'][0]
    name_city: str = GeoObject['GeoObject']['name']
    description: str = GeoObject['GeoObject']['description']
    point: dict = GeoObject['GeoObject']['Point']

    longitude, latitude = point.get('pos').split()

    city_info = {
        'name': name_city,
        'country': description,
        'latitude': Decimal(latitude),
        'longitude': Decimal(longitude),
    }
    
    return city_info


async def add_city_info_db(name_city: str, session: AsyncSession) -> dict:
    '''записыват данные горда в бд'''
    
    city_data = await get_json_data(name_city)

    stmt = insert(CityModel).values(**city_data) 
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.IntegrityError:
        pass

    return {'status': status.HTTP_200_OK}



async def get_city(name_city: str, session: AsyncSession) -> dict:
    '''делает запрос в бд и возвращает информацию о городе'''

    query = select(CityModel).where(CityModel.name == name_city)
    result = await session.execute(query)
    
    city_info = result.scalar_one_or_none()

    if city_info is None:
        return {
            'status': status.HTTP_404_NOT_FOUND,
            'data': None
            }
    
    
    return {
            'status': status.HTTP_200_OK,
            'data': city_info
            }


async def del_city(name: str, session: AsyncSession) -> dict:
    '''удаляет запись из бд возвращает удаленный объект'''
    city_response = await get_city(name_city=name, session=session)
    
    if city_response.get('status') is status.HTTP_200_OK:
        await session.delete(city_response.get('data'))
        await session.commit()
    
    return {'status': status.HTTP_200_OK}



async def search_nearest_cities(point: Coordinate, session: AsyncSession) -> dict:
    '''получение двух ближайших гороодов из бд'''

    query = select(
    CityModel.name,
    (func.acos(
        func.cos(func.radians(point.geo_lat)) * func.cos(func.radians(CityModel.latitude)) *
        func.cos(func.radians(CityModel.longitude) - func.radians(point.geo_lon)) +
        func.sin(func.radians(point.geo_lat)) * func.sin(func.radians(CityModel.latitude))
    ) * 6371).label('distance')
    ).order_by('distance').limit(2)

    res = await session.execute(query)
    
    data = res.fetchall()
    response = {
        'status': '',
        'data': []
        }
    
    if data:
        response['status'] = status.HTTP_200_OK
        for name_city in data:
            response['data'].append(name_city[0])
    else: 
        response['status'] = status.HTTP_404_NOT_FOUND
    
    return response
    

