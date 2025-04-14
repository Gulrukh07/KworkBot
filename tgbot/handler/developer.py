from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.buttons.reply import make_reply_button
from tgbot.states import DeveloperForm


async def developer_button_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({'role': message.text})
    buttons = ['⬅️Back']
    sizes = [1]
    markup = make_reply_button(buttons, sizes)
    await state.set_state(DeveloperForm.name)
    await message.answer('Enter your fullname:', reply_markup=markup)
