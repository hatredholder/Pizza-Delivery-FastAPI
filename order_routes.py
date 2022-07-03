from fastapi import APIRouter


order_router = APIRouter(
    prefix="/order",
    tags=['Orders']
)


@order_router.get('/')
async def hello():
    return {'hello': 'world'}