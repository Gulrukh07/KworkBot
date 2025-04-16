from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import User
from tgbot.buttons.reply import make_reply_button
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm, CustomerForm


@dp.message(DeveloperForm.main_panel, F.text == 'Back to Register')
@dp.message(CustomerForm.main_panel, F.text == 'Back to Register')
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    buttons = ['Developer', 'Customer']
    sizes = [2]
    markup = make_reply_button(buttons, sizes)
    await message.answer(f"Hello, {message.from_user.full_name}!")
    user = User(chat_id=message.from_user.id)
    await message.answer(f"Who are You?", reply_markup=markup)



@dp.message(CustomerForm.main_panel, F.text == 'Back to Register')
async def customer_button_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await command_start_handler(message, state)
