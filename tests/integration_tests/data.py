from uuid import uuid4

# Endpoints
ID = uuid4()
PREFIX = '/api/v1/'
ENDPOINT_MENU = f'{PREFIX}menus'
ENDPOINT_SUBMENU = ENDPOINT_MENU + '/{id}/submenus'
ENDPOINT_SUBMENU_DEFAULT = ENDPOINT_SUBMENU.format(id=ID)
ENDPOINT_DISH = ENDPOINT_SUBMENU_DEFAULT + '/{id}/dishes'
ENDPOINT_DISH_DEFAULT = ENDPOINT_DISH.format(id=ID)

# Messages
MENU_NOT_FOUND_MSG = 'menu not found'
MENU_ALREADY_EXISTS_MSG = 'Меню с таким заголовком уже существует.'
MENU_MSG_PACK = (MENU_ALREADY_EXISTS_MSG, MENU_NOT_FOUND_MSG)

SUBMENU_NOT_FOUND_MSG = 'submenu not found'
SUBMENU_ALREADY_EXISTS_MSG = 'Подменю с таким заголовком уже существует.'
SUBMENU_MSG_PACK = (SUBMENU_ALREADY_EXISTS_MSG, SUBMENU_NOT_FOUND_MSG)

DISH_NOT_FOUND_MSG = 'dish not found'
DISH_ALREADY_EXISTS_MSG = 'Блюдо с таким заголовком уже существует.'
DISH_MSG_PACK = (DISH_ALREADY_EXISTS_MSG, DISH_NOT_FOUND_MSG)

# MENU Data
MENU_POST_PAYLOAD = {'title': 'My menu 1',
                     'description': 'My menu description 1'}
MENU_PATCH_PAYLOAD = {'title': 'My updated menu 1',
                      'description': 'My updated menu description 1'}
CREATED_MENU = {'title': 'My menu 1',
                'description': 'My menu description 1',
                'submenus_count': 0,
                'dishes_count': 0}
EXPECTED_MENU = {'title': 'My menu 1',
                 'description': 'My menu description 1',
                 'submenus_count': 1,
                 'dishes_count': 1}
UPDATED_MENU = {'title': 'My updated menu 1',
                'description': 'My updated menu description 1',
                'submenus_count': 1,
                'dishes_count': 1}
DELETED_MENU = {'status': True, 'message': 'The menu has been deleted'}

# SUBMENU Data
SUBMENU_POST_PAYLOAD = {'title': 'My submenu 1',
                        'description': 'My submenu description 1'}
SUBMENU_PATCH_PAYLOAD = {'title': 'My updated submenu 1',
                         'description': 'My updated submenu description 1'}
CREATED_SUBMENU = {'title': 'My submenu 1',
                   'description': 'My submenu description 1',
                   'dishes_count': 0}
EXPECTED_SUBMENU = {'title': 'My submenu 1',
                    'description': 'My submenu description 1',
                    'dishes_count': 1}
UPDATED_SUBMENU = {'title': 'My updated submenu 1',
                   'description': 'My updated submenu description 1',
                   'dishes_count': 1}
DELETED_SUBMENU = {'status': True, 'message': 'The submenu has been deleted'}

# DISH Data
DISH_POST_PAYLOAD = {'title': 'My dish 1',
                     'description': 'My dish description 1',
                     'price': '12.50'}
DISH_PATCH_PAYLOAD = {'title': 'My updated dish 1',
                      'description': 'My updated dish description 1',
                      'price': '14.5000'}
CREATED_DISH = {'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '12.50'}
UPDATED_DISH = {'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '14.50'}
DELETED_DISH = {'status': True, 'message': 'The dish has been deleted'}
