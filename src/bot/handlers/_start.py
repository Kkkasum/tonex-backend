from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.keyboards import start_kb


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text='Web App', reply_markup=start_kb())
