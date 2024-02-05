from uuid import UUID

from fastapi import APIRouter

from app.api.endpoints import const as u
from app.core.config import settings
from app.schemas import schemas
from app.services.services import dish_service

router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Dishes'])

NAME = 'блюда'
SUM_ALL_ITEMS = u.SUM_ALL_ITEMS.format('блюд')
SUM_ITEM = u.SUM_ITEM.format('блюдо')
SUM_CREATE_ITEM = u.SUM_CREATE_ITEM.format(NAME)
SUM_UPDATE_ITEM = u.SUM_UPDATE_ITEM.format(NAME)
SUM_DELETE_ITEM = u.SUM_DELETE_ITEM.format(NAME)


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[schemas.DishOut],
    summary=SUM_ALL_ITEMS,
    description=(f'{settings.ALL_USERS} {SUM_ALL_ITEMS}'))
async def get_all_(submenu_id: str, dish_service: dish_service):
    return await dish_service.get(submenu_id=submenu_id)


@router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=201,
    response_model=schemas.DishOut,
    summary=SUM_CREATE_ITEM,
    description=(f'{settings.AUTH_ONLY} {SUM_CREATE_ITEM}'))
async def create_(submenu_id: str,
                  payload: schemas.DishIn,
                  dish_service: dish_service):
    return await dish_service.create(**payload.model_dump(), submenu_id=submenu_id)


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{item_id}',
    response_model=schemas.DishOut,
    summary=SUM_ITEM,
    description=(f'{settings.ALL_USERS} {SUM_ITEM}'))
async def get_(item_id: UUID, dish_service: dish_service):
    return await dish_service.get(id=item_id, exception=True)


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{item_id}',
    response_model=schemas.DishOut,
    summary=SUM_UPDATE_ITEM,
    description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_ITEM}'))
async def update_(item_id: UUID,
                  payload: schemas.DishPatch,
                  dish_service: dish_service):
    return await dish_service.update(id=item_id, **payload.model_dump(exclude_defaults=True,
                                                                      exclude_none=True,
                                                                      exclude_unset=True))


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/dishes/{item_id}',
    summary=SUM_DELETE_ITEM,
    description=(f'{settings.SUPER_ONLY} {SUM_DELETE_ITEM}'))
async def delete_(item_id: UUID, dish_service: dish_service):
    return await dish_service.delete(id=item_id)
