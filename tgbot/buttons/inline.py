from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_button(btns, sizes, user_id=None):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=btn, callback_data=f"{btn}_{str(user_id)}") for btn in btns])
    ikb.adjust(*sizes)
    return ikb.as_markup(resize_keyboard=True)


def admin_contact():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='Admin', url='https://t.me/KhalilovnaG')])
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)

def developer_response(customer_id,project_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text= 'Accept', callback_data=f'Accepted_{customer_id}_{project_id}')])
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)

def chat_with_developer(developer_username):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text='Developer', url=f"https://t.me/{developer_username}"))
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)


