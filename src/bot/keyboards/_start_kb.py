from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, WebAppInfo


def start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Web App',
        web_app=WebAppInfo(url='https://roaring-bienenstitch-1d676b.netlify.app')
    )

    return builder.as_markup()
