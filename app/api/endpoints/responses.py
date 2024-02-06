from pydantic import BaseModel


def get_400(name: str):
    class Message(BaseModel):
        detail: str = f'{name} с таким заголовком уже существует.'

    return {400: {'model': Message, 'description': 'The item already exists'}}


def get_404(name: str):
    class Message(BaseModel):
        detail: str = f'{name} not found'

    return {404: {'model': Message, 'description': 'The item was not found'}}
