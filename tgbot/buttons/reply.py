from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def make_reply_button(btns, sizes, lang: str = None):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=btn, locale=lang) for btn in btns])
    rkb.adjust(*sizes)
    return rkb.as_markup(resize_keyboard=True)


def rkb_with_contact():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text='Contact', request_contact=True),
              KeyboardButton(text='⬅️Back')])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard=True)


btns = ['⬅️Back']
size = [1]
back_markup = make_reply_button(btns, size)

buttons = ['FrontEnd', 'BackEnd', 'Android', 'Fullstack', '⬅️Back']
sizes = [2, 2]
occupation_markup = make_reply_button(buttons, sizes)


def change_language_button():
    btns = ['uz', 'ru', 'en']
    size = [3]
    ikb = InlineKeyboardBuilder()
    for btn in btns:
        ikb.add(InlineKeyboardButton(text=f"{btn}", callback_data=f"lang_{btn}"))

    return ikb.as_markup()
