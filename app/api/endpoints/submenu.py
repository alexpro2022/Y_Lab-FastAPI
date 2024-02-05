from uuid import UUID

from fastapi import APIRouter

from app.api.endpoints import const as u
from app.core.config import settings
from app.schemas import schemas
from app.services.services import submenu_service

router = APIRouter(prefix=f'{settings.URL_PREFIX}menus', tags=['Submenus'])

NAME = 'подменю'
SUM_ALL_ITEMS = u.SUM_ALL_ITEMS.format(NAME)
SUM_ITEM = u.SUM_ITEM.format(NAME)
SUM_CREATE_ITEM = u.SUM_CREATE_ITEM.format(NAME)
SUM_UPDATE_ITEM = u.SUM_UPDATE_ITEM.format(NAME)
SUM_DELETE_ITEM = u.SUM_DELETE_ITEM.format(NAME)


@router.get(
    '/{menu_id}/submenus',
    response_model=list[schemas.SubmenuOut],
    summary=SUM_ALL_ITEMS,
    description=(f'{settings.ALL_USERS} {SUM_ALL_ITEMS}'))
async def get_all_(menu_id: UUID, submenu_service: submenu_service):
    return await submenu_service.get(menu_id=menu_id)


@router.post(
    '/{menu_id}/submenus',
    status_code=201,
    response_model=schemas.SubmenuOut,
    summary=SUM_CREATE_ITEM,
    description=(f'{settings.AUTH_ONLY} {SUM_CREATE_ITEM}'))
async def create_(menu_id: UUID,
                  payload: schemas.SubmenuIn,
                  submenu_service: submenu_service):
    return await submenu_service.create(**payload.model_dump(), menu_id=menu_id)


@router.get(
    '/{menu_id}/submenus/{item_id}',
    response_model=schemas.SubmenuOut,
    summary=SUM_ITEM,
    description=(f'{settings.ALL_USERS} {SUM_ITEM}'))
async def get_(item_id: UUID, submenu_service: submenu_service):
    return await submenu_service.get(id=item_id, exception=True)


@router.patch(
    '/{menu_id}/submenus/{item_id}',
    response_model=schemas.SubmenuOut,
    summary=SUM_UPDATE_ITEM,
    description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_ITEM}'))
async def update_(item_id: UUID,
                  payload: schemas.SubmenuPatch,
                  submenu_service: submenu_service):
    return await submenu_service.update(id=item_id, **payload.model_dump(exclude_defaults=True,
                                                                         exclude_none=True,
                                                                         exclude_unset=True))


@router.delete(
    '/{menu_id}/submenus/{item_id}',
    summary=SUM_DELETE_ITEM,
    description=(f'{settings.SUPER_ONLY} {SUM_DELETE_ITEM}'))
async def delete_(item_id: UUID, submenu_service: submenu_service):
    return await submenu_service.delete(id=item_id)
