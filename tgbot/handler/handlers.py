from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.buttons.reply import make_reply_button
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm, CustomerForm


@dp.message(CustomerForm.main_panel, F.text == '⬅️Back')
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    buttons = ['Developer', 'Customer']
    sizes = [2]
    markup = make_reply_button(buttons, sizes)
    await state.set_state(CustomerForm.start)
    await state.set_state(DeveloperForm.start)
    await message.answer(f"Hello, {message.from_user.full_name}!")
    await message.answer(f"Who are You?", reply_markup=markup)

# @dp.message(F.text == "Bact To Register")
# async def back_to_register(message: Message):
#     User(chat_id=message.chat.id).delete()
#     await message.answer("/start")
