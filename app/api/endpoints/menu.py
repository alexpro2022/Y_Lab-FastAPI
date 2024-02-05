from uuid import UUID

from fastapi import APIRouter

from app.api.endpoints import const as u
from app.core.config import settings
from app.schemas import schemas
# from app.repositories.db_repository import menu_service
from app.services.services import menu_service

router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Menus'])

NAME = 'меню'
SUM_ALL_ITEMS = u.SUM_ALL_ITEMS.format(NAME)
SUM_ITEM = u.SUM_ITEM.format(NAME)
SUM_CREATE_ITEM = u.SUM_CREATE_ITEM.format(NAME)
SUM_UPDATE_ITEM = u.SUM_UPDATE_ITEM.format(NAME)
SUM_DELETE_ITEM = u.SUM_DELETE_ITEM.format(NAME)
SUM_FULL_LIST = f'Полный список {NAME}.'


@router.get(
    '',
    response_model=list[schemas.MenuOut],
    summary=SUM_ALL_ITEMS,
    description=(f'{settings.ALL_USERS} {SUM_ALL_ITEMS}'))
async def get_all_(menu_service: menu_service):
    return await menu_service.get()


@router.post(
    '',
    status_code=201,
    response_model=schemas.MenuOut,
    summary=SUM_CREATE_ITEM,
    description=(f'{settings.AUTH_ONLY} {SUM_CREATE_ITEM}'))
async def create_(payload: schemas.MenuIn, menu_service: menu_service):
    return await menu_service.create(**payload.model_dump())


@router.get(
    '/{item_id}',
    response_model=schemas.MenuOut,
    summary=SUM_ITEM,
    description=(f'{settings.ALL_USERS} {SUM_ITEM}'))
async def get_(item_id: UUID, menu_service: menu_service):
    return await menu_service.get(id=item_id, exception=True)


@router.patch(
    '/{item_id}',
    response_model=schemas.MenuOut,
    summary=SUM_UPDATE_ITEM,
    description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_ITEM}'))
async def update_(item_id: UUID, payload: schemas.MenuPatch, menu_service: menu_service):
    return await menu_service.update(id=item_id, **payload.model_dump(exclude_defaults=True,
                                                                      exclude_none=True,
                                                                      exclude_unset=True))


@router.delete(
    '/{item_id}',
    summary=SUM_DELETE_ITEM,
    description=(f'{settings.SUPER_ONLY} {SUM_DELETE_ITEM}'))
async def delete_(item_id: UUID, menu_service: menu_service):
    return await menu_service.delete(id=item_id)
