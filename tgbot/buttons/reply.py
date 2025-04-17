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

btns = ['⬅️Back']
size = [1]
back_markup = make_reply_button(btns, size)

buttons = ['FrontEnd', 'BackEnd', 'Android', 'Fullstack','⬅️Back']
sizes = [2,2]
occupation_markup = make_reply_button(buttons,sizes)
