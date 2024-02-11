from uuid import UUID

from fastapi import APIRouter

from app.api.endpoints import const as u
from app.api.endpoints.responses import get_400, get_404
from app.core.config import settings
from app.models import Dish
from app.schemas import schemas
from app.services.services import dish_service

router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Dishes'])

NAME = 'блюда'
SUM_ALL_ITEMS = u.SUM_ALL_ITEMS.format('блюд')
SUM_ITEM = u.SUM_ITEM.format('блюдо')
SUM_CREATE_ITEM = u.SUM_CREATE_ITEM.format(NAME)
SUM_UPDATE_ITEM = u.SUM_UPDATE_ITEM.format(NAME)
SUM_DELETE_ITEM = u.SUM_DELETE_ITEM.format(NAME)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes',
            response_model=list[schemas.DishOut],
            summary=SUM_ALL_ITEMS,
            description=(f'{settings.ALL_USERS} {SUM_ALL_ITEMS}'))
async def get_all_dishes(menu_id: UUID, submenu_id: UUID, dish_service: dish_service) -> list[Dish]:
    cache_key = f'{menu_id}:{submenu_id}'
    return await dish_service.get(submenu_id=submenu_id, cache_key=cache_key)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes',
             status_code=201,
             responses={**get_400('Блюдо')},
             response_model=schemas.DishOut,
             summary=SUM_CREATE_ITEM,
             description=(f'{settings.AUTH_ONLY} {SUM_CREATE_ITEM}'))
async def create_dish(menu_id: UUID, submenu_id: UUID,
                      payload: schemas.DishIn,
                      dish_service: dish_service) -> Dish:
    cache_key = f'{menu_id}:{submenu_id}'
    return await dish_service.create(**payload.model_dump(), submenu_id=submenu_id, cache_key=cache_key)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            response_model=schemas.DishOut,
            responses={**get_404('dish')},
            summary=SUM_ITEM,
            description=(f'{settings.ALL_USERS} {SUM_ITEM}'))
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish_service: dish_service) -> Dish:
    cache_key = f'{menu_id}:{submenu_id}:{dish_id}'
    return await dish_service.get(id=dish_id, cache_key=cache_key, exception=True)  # type: ignore [return-value]


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
              response_model=schemas.DishOut,
              responses={**get_404('dish')},
              summary=SUM_UPDATE_ITEM,
              description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_ITEM}'))
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID,
                      payload: schemas.DishPatch,
                      dish_service: dish_service) -> Dish:
    cache_key = f'{menu_id}:{submenu_id}:{dish_id}'
    return await dish_service.update(id=dish_id, cache_key=cache_key,
                                     **payload.model_dump(exclude_defaults=True,
                                                          exclude_none=True,
                                                          exclude_unset=True))


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
               response_model=schemas.Delete,
               responses={**get_404('dish')},
               summary=SUM_DELETE_ITEM,
               description=(f'{settings.SUPER_ONLY} {SUM_DELETE_ITEM}'))
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID,
                      dish_service: dish_service) -> dict[str, bool | str]:
    cache_key = f'{menu_id}:{submenu_id}:{dish_id}'
    return await dish_service.delete(id=dish_id, cache_key=cache_key)
