from typing import Any, AsyncGenerator

from httpx import AsyncClient

from tests.fixtures import data as d
from tests.integration_tests.utils import (
    Json,
    check_dish_updated,
    del_dish,
    del_menu,
    del_submenu,
    get_dishes,
    get_menu,
    get_menus,
    get_submenu,
    get_submenus,
    post_dish,
    post_menu,
    post_submenu,
)


async def test_scenario(init_db: AsyncGenerator, async_client: AsyncClient, mock_dish_discount) -> None:
    menu: Json = await post_menu(async_client)
    menu_id = menu['id']
    submenu: Json = await post_submenu(async_client, menu_id)
    submenu_id = submenu['id']
    await post_dish(async_client, menu_id, submenu_id)
    await post_dish(  # must use different payload as the title is unique, so check_func also different
        async_client, menu_id, submenu_id, d.DISH_PATCH_PAYLOAD, check_dish_updated)
    await get_menu(async_client, menu_id, submenus_count=1, dishes_count=2)
    await get_submenu(async_client, menu_id, submenu_id, dishes_count=2)
    await del_submenu(async_client, menu_id, submenu_id)
    await get_submenus(async_client, menu_id, [])
    await get_dishes(async_client, menu_id, submenu_id, [])
    await get_menu(async_client, menu_id)
    await del_menu(async_client, menu_id)
    await get_menus(async_client, [])


async def test_services(init_db: AsyncGenerator, async_client: AsyncClient, mock_dish_discount) -> None:
    async def init() -> tuple[Any, ...]:
        menu: Json = await post_menu(async_client)
        menu_id = menu['id']
        submenu: Json = await post_submenu(async_client, menu_id)
        submenu_id = submenu['id']
        dish: Json = await post_dish(async_client, menu_id, submenu_id)
        await post_dish(  # must use different payload as the title is unique, so check_func also different
            async_client, menu_id, submenu_id, d.DISH_PATCH_PAYLOAD, check_dish_updated)
        # Testing refresh_parent_cache on create
        await get_menu(async_client, menu_id, submenus_count=1, dishes_count=2)
        await get_submenu(async_client, menu_id, submenu_id, dishes_count=2)
        return menu_id, submenu_id, dish['id']

    async def cleanup() -> None:
        await del_menu(async_client, menu_id)
        await get_menus(async_client, [])

    # Testing menu delete orphans
    menu_id, submenu_id, _ = await init()
    await del_menu(async_client, menu_id)
    await get_menus(async_client, [])
    await get_submenus(async_client, menu_id, [])
    await get_dishes(async_client, menu_id, submenu_id, [])

    # Testing submenu delete orphans
    menu_id, submenu_id, _ = await init()
    await del_submenu(async_client, menu_id, submenu_id)
    await get_submenus(async_client, menu_id, [])
    await get_dishes(async_client, menu_id, submenu_id, [])
    await cleanup()

    # Testing refresh_parent_cache on delete submenu
    menu_id, submenu_id, _ = await init()
    await del_submenu(async_client, menu_id, submenu_id)
    await get_menu(async_client, menu_id)  # submenus_count=0, dishes_count=0 by default
    await cleanup()

    # Testing refresh_parent_cache on delete dish
    menu_id, submenu_id, dish_id = await init()
    await del_dish(async_client, submenu_id, dish_id)
    await get_menu(async_client, menu_id, submenus_count=1, dishes_count=1)
    await get_submenu(async_client, menu_id, submenu_id, dishes_count=1)
    await cleanup()
