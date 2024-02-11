from uuid import UUID

from fastapi import APIRouter

from app.api.endpoints import const as u
from app.api.endpoints.responses import get_400, get_404
from app.core.config import settings
from app.models import Submenu
from app.schemas import schemas
from app.services.services import submenu_service

router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Submenus'])

NAME = 'подменю'
SUM_ALL_ITEMS = u.SUM_ALL_ITEMS.format(NAME)
SUM_ITEM = u.SUM_ITEM.format(NAME)
SUM_CREATE_ITEM = u.SUM_CREATE_ITEM.format(NAME)
SUM_UPDATE_ITEM = u.SUM_UPDATE_ITEM.format(NAME)
SUM_DELETE_ITEM = u.SUM_DELETE_ITEM.format(NAME)


@router.get('/{menu_id}/submenus',
            response_model=list[schemas.SubmenuOut],
            summary=SUM_ALL_ITEMS,
            description=(f'{settings.ALL_USERS} {SUM_ALL_ITEMS}'))
async def get_all_submenus(menu_id: UUID, submenu_service: submenu_service) -> list[Submenu]:
    return await submenu_service.get(menu_id=menu_id, cache_key=menu_id)


@router.post('/{menu_id}/submenus',
             status_code=201,
             responses={**get_400('Подменю')},
             response_model=schemas.SubmenuOut,
             summary=SUM_CREATE_ITEM,
             description=(f'{settings.AUTH_ONLY} {SUM_CREATE_ITEM}'))
async def create_submenu(menu_id: UUID,
                         payload: schemas.SubmenuIn,
                         submenu_service: submenu_service) -> Submenu:
    return await submenu_service.create(menu_id=menu_id, cache_key=menu_id,
                                        **payload.model_dump())


@router.get('/{menu_id}/submenus/{submenu_id}',
            response_model=schemas.SubmenuOut,
            responses={**get_404('submenu')},
            summary=SUM_ITEM,
            description=(f'{settings.ALL_USERS} {SUM_ITEM}'))
async def get_submenu(menu_id: UUID, submenu_id: UUID, submenu_service: submenu_service) -> Submenu:
    cache_key = f'{menu_id}:{submenu_id}'
    return await submenu_service.get(id=submenu_id, cache_key=cache_key, exception=True)  # type: ignore [return-value]


@router.patch('/{menu_id}/submenus/{submenu_id}',
              response_model=schemas.SubmenuOut,
              responses={**get_404('submenu')},
              summary=SUM_UPDATE_ITEM,
              description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_ITEM}'))
async def update_submenu(menu_id: UUID, submenu_id: UUID,
                         payload: schemas.SubmenuPatch,
                         submenu_service: submenu_service) -> Submenu:
    cache_key = f'{menu_id}:{submenu_id}'
    return await submenu_service.update(id=submenu_id, cache_key=cache_key,
                                        **payload.model_dump(exclude_defaults=True,
                                                             exclude_none=True,
                                                             exclude_unset=True))


@router.delete('/{menu_id}/submenus/{submenu_id}',
               response_model=schemas.Delete,
               responses={**get_404('submenu')},
               summary=SUM_DELETE_ITEM,
               description=(f'{settings.SUPER_ONLY} {SUM_DELETE_ITEM}'))
async def delete_submenu(menu_id: UUID, submenu_id: UUID, submenu_service: submenu_service) -> dict[str, bool | str]:
    cache_key = f'{menu_id}:{submenu_id}'
    return await submenu_service.delete(id=submenu_id, cache_key=cache_key)
