from fastapi import APIRouter

# from app import schemas
from app.core.config import settings

# from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Menus'])
