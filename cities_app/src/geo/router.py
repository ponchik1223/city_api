import fastapi
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from .schemas import City, Coordinate
from .utils import add_city_info_db, get_city, del_city, search_nearest_cities
from src.database import get_async_session

geo_router = fastapi.APIRouter()


@geo_router.get('/city/{name_city}')
async def get_city_info(name_city: str, session: AsyncSession = Depends(get_async_session)):
    '''эндпоинт для получение информации о городе'''
    respone = await get_city(session=session, name_city=name_city)
    return respone

@geo_router.post('/city/add')
async def add_city(city: City, session: AsyncSession = Depends(get_async_session)):
    '''эндпоинт добавления города в бд'''
    response = await add_city_info_db(name_city=city.name_city, session=session)
    
    return response


@geo_router.delete('/city/del')
async def delete_city(city: City, session: AsyncSession = Depends(get_async_session)):
    '''эндпоинт для удаления города из бд'''
    response = await del_city(name=city.name_city, session=session)

    return response


@geo_router.post('/city/nearest_cities')
async def nearest_cities(coordinate: Coordinate, session: AsyncSession = Depends(get_async_session)):
    '''эндпоинт для получения ближайших городов по координатам (широта/долгота)'''
    response = await search_nearest_cities(point=coordinate, session=session)
    
    return response