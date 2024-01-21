from fastapi import APIRouter

from app.api.endpoints import example

main_router = APIRouter()


for router in (
    example.router,
):
    main_router.include_router(router)
