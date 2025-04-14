from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_reply_button(btns, sizes):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=btn) for btn in btns])
    rkb.adjust(*sizes)
    return rkb.as_markup(resize_keyboard = True)


def rkb_with_contact():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text='Contact', request_contact=True),
              KeyboardButton(text='⬅️Back')])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard = True)


