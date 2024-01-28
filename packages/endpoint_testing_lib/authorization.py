from .utils import AsyncClient, HTTPStatus, assert_status


async def get_registered(async_client: AsyncClient, user: dict) -> None:
    response = await async_client.post('/auth/register', json=user)
    assert_status(response, (HTTPStatus.OK, HTTPStatus.CREATED))
    auth_user: dict = response.json()
    assert auth_user['id']
    assert auth_user['email'] == user['email']
    assert auth_user['is_active']
    assert not auth_user['is_superuser']
    assert not auth_user['is_verified']


async def get_auth_user_token(async_client: AsyncClient, user: dict | None, registration: bool = True) -> str | None:
    if user is None:
        return None
    if registration:
        await get_registered(async_client, user)
    user = user.copy()
    user['username'] = user['email']
    response = await async_client.post('/auth/jwt/login', data=user)
    assert_status(response, HTTPStatus.OK)
    token = response.json()['access_token']
    assert isinstance(token, str)
    return token


def get_headers(token: str | None) -> dict[str, str] | None:
    return {'Authorization': f'Bearer {token}'} if token is not None else None
