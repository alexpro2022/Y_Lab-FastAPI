# Проект Меню ресторана:

### Simple RESTful API using FastAPI for a restaurant menu application

[Тестовое задание](https://learning-platform.ylab.website/my-homeworks/16)

<details><summary>ДЗ №1</summary>
<h1></h1>

☑ Написать проект на FastAPI с использованием PostgreSQL в качестве БД.

☑ В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции.

<h1></h1>
</details>

<br>

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Запуск тестов](#запуск-тестов)
- [Запуск тестового сценария](#запуск-тестового-сценария)
- [Запуск приложения](#запуск-приложения)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>

## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?logo=Pydantic)](https://docs.pydantic.dev/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v2.0-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)

[⬆️Оглавление](#оглавление)

</details>

<br>

## Описание работы

Даны 3 сущности:
  - Меню,
  - Подменю,
  - Блюдо.

Зависимости:
  - У меню есть подменю, которые к нему привязаны.
  - У подменю есть блюда, которые к нему привязаны.

Условия:
  - Блюдо не может быть привязано напрямую к меню, минуя подменю.
  - Блюдо не может находиться в 2-х подменю одновременно.
  - Подменю не может находиться в 2-х меню одновременно.
  - Если удалить меню, должны удалиться все подменю и блюда этого меню.
  - Если удалить подменю, должны удалиться все блюда этого подменю.
  - Цены блюд выводить с округлением до 2 знаков после запятой.
  - Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
  - Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.

Swagger позволяет осуществлять http-запросы к работающему сервису, тем самым можно управлять этими сущностями в рамках политики сервиса.

[⬆️Оглавление](#оглавление)

<br>

## Установка приложения:

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

```bash
docker --version && docker-compose --version
```
<h1></h1></details>

<!--details><summary>Локальный запуск</summary-->
<br>

Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/Y_Lab-FastAPI.git
cd Y_Lab-FastAPI
cp env_example .env
nano .env
```

[⬆️Оглавление](#оглавление)

<br>

## Запуск приложения:

1. Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/docker-compose.yml up -d --build
```
  Проект будет развернут в docker-контейнерах по адресу http://127.0.0.1:8000.

  Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://127.0.0.1:8000/docs .

2. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f docker/docker-compose.yml down
```
Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/docker-compose.yml down -v
```

[⬆️Оглавление](#оглавление)

<br>

## Удаление приложения:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr Y_Lab-FastAPI
```

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#проект-меню-ресторана)
