from uuid import UUID

from fastapi import APIRouter
from app.celery_tasks.utils import load_data
from app.api.endpoints import const as u
from app.api.endpoints.responses import get_400, get_404
from app.core.config import settings
from app.models import Menu
from app.repositories.db_repository import menu_crud
from app.repositories.full_list import get_full_list
from app.schemas import schemas
from app.services.services import menu_service

router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Menus'])

NAME = 'меню'
SUM_ALL_ITEMS = u.SUM_ALL_ITEMS.format(NAME)
SUM_ITEM = u.SUM_ITEM.format(NAME)
SUM_CREATE_ITEM = u.SUM_CREATE_ITEM.format(NAME)
SUM_UPDATE_ITEM = u.SUM_UPDATE_ITEM.format(NAME)
SUM_DELETE_ITEM = u.SUM_DELETE_ITEM.format(NAME)
SUM_FULL_LIST = f'Полный список {NAME}.'


@router.get('',
            response_model=list[schemas.MenuOut],
            summary=SUM_ALL_ITEMS,
            description=(f'{settings.ALL_USERS} {SUM_ALL_ITEMS}'))
async def get_all_menus(menu_service: menu_service) -> list[Menu]:
    await load_data()
    return await menu_service.get()


@router.get('-full-list',
            response_model=list[schemas.FullList],
            summary=SUM_FULL_LIST,
            description=(f'{settings.SUPER_ONLY} {SUM_FULL_LIST}'))
async def get_full_list_(menu_crud: menu_crud):
    return await get_full_list(menu_crud)


@router.post('',
             status_code=201,
             response_model=schemas.MenuOut,
             responses={**get_400('Меню')},
             summary=SUM_CREATE_ITEM,
             description=(f'{settings.AUTH_ONLY} {SUM_CREATE_ITEM}'))
async def create_menu(payload: schemas.MenuIn, menu_service: menu_service) -> Menu:
    return await menu_service.create(**payload.model_dump())


@router.get('/{menu_id}',
            response_model=schemas.MenuOut,
            responses={**get_404('menu')},
            summary=SUM_ITEM,
            description=(f'{settings.ALL_USERS} {SUM_ITEM}'))
async def get_menu(menu_id: UUID, menu_service: menu_service) -> Menu:
    return await menu_service.get(id=menu_id, exception=True)  # type: ignore [return-value]


@router.patch('/{menu_id}',
              response_model=schemas.MenuOut,
              responses={**get_404('menu')},
              summary=SUM_UPDATE_ITEM,
              description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_ITEM}'))
async def update_menu(menu_id: UUID, payload: schemas.MenuPatch, menu_service: menu_service) -> Menu:
    return await menu_service.update(id=menu_id, **payload.model_dump(exclude_defaults=True,
                                                                      exclude_none=True,
                                                                      exclude_unset=True))


@router.delete('/{menu_id}',
               response_model=schemas.Delete,
               responses={**get_404('menu')},
               summary=SUM_DELETE_ITEM,
               description=(f'{settings.SUPER_ONLY} {SUM_DELETE_ITEM}'))
async def delete_menu(menu_id: UUID, menu_service: menu_service) -> dict[str, bool | str]:
    return await menu_service.delete(id=menu_id)
