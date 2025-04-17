from aiogram.types import  InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_button(btns, sizes):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=btn) for btn in btns])
    ikb.adjust(*sizes)
    return ikb.as_markup(resize_keyboard = True)

def admin_contact():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text = 'Admin', url='https://t.me/KhalilovnaG')])
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)