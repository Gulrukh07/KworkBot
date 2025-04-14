from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import User
# from tgbot.buttons.reply import rkb_with_contact, make_reply_button
from tgbot.states import DeveloperForm, CustomerForm
from .handlers import dp
#
# btns = ['⬅️Back']
# size = [1]
# back_markup = make_reply_button(btns, size)


# @dp.message(CustomerForm.main_panel, F.text)  # noqa
