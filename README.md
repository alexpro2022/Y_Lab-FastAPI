# Проект Меню ресторана:

### Simple RESTful API using FastAPI for a restaurant menu application

[Тестовое задание](https://learning-platform.ylab.website/my-homeworks/16)

<details><summary>ДЗ №1</summary>
<h1></h1>

☑ Написать проект на FastAPI с использованием PostgreSQL в качестве БД.

☑ В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции.

<h1></h1>
</details>

<!--details><summary>ДЗ №2</summary-->
ДЗ №2
<h1></h1>

☑ В этом домашнем задании надо написать тесты для ранее разработанных эндпоинтов вашего API после вебинара №1.

☑ Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде `docker-compose up -d` или той которая описана вами в `README.md`.

☑ Образы для Docker:
  - (API) 	python:3.10-slim
  - (DB) 	postgres:15.1-alpine

☑ Написать CRUD тесты для ранее разработанного API с помощью библиотеки `pytest`.

☑ Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в `README.md`.

☑ Если FastAPI синхронное - тесты синхронные, если асинхронное - тесты асинхронные.

☑ Реализовать вывод количества подменю  и блюд для Меню через один (сложный) ORM запрос:
    [ссылка](https://github.com/alexpro2022/Y_Lab-FastAPI/blob/219261c0d5e61b4172a441b4725879841af8f77b/app/repositories/db_repository.py#L24)

☑ Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из `Postman` с помощью `pytest`.

<h1></h1>
<!--/details-->


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
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=codecov)](https://pytest-cov.readthedocs.io/en/latest/)


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

## Запуск тестов:

Из корневой директории проекта выполните команду запуска тестов:
```bash
docker compose -f docker/tests/test.docker-compose.yml --env-file .env up --build --abort-on-container-exit && \
docker compose -f docker/tests/test.docker-compose.yml --env-file .env down -v

```
После прохождения тестов в консоль будет выведен отчет pytest и coverage.

[⬆️Оглавление](#оглавление)

<br>

## Запуск тестового сценария

Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/tests/test_scenario.docker-compose.yml --env-file .env up --build --abort-on-container-exit && \
docker compose -f docker/tests/test_scenario.docker-compose.yml --env-file .env down -v

```
После прохождения теста в консоль будет выведен отчет pytest.

[⬆️Оглавление](#оглавление)

<br>

## Запуск приложения:

1. Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env up -d --build
```
  Проект будет развернут в docker-контейнерах по адресу http://127.0.0.1:8000.

  Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://127.0.0.1:8000/docs.

2. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env down
```
Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env down -v
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
