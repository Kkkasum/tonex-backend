from aiogram import Dispatcher

from ._start import router as start_router


def include_routers(dp: Dispatcher):
    dp.include_routers(
        start_router
    )
