from fastapi import APIRouter

from src.app.backend.jetton import jetton_router
from src.app.backend.users import users_router


router = APIRouter()

router.include_router(jetton_router, prefix='/jetton', tags=['Jetton'])
router.include_router(users_router, prefix='/users', tags=['Users'])
