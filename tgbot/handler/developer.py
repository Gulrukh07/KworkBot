from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import Developer
from tgbot.buttons.reply import rkb_with_contact, occupation_markup, make_reply_button
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm


@dp.message(DeveloperForm.occupation, F.text == '⬅️Back')
@dp.message(DeveloperForm.main_panel, F.text == '⬅️Back')
@dp.message(DeveloperForm.contact, F.text == '⬅️Back')
@dp.message(F.text == 'Developer')
async def developer_button_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({'role': message.text})
    await state.set_state(DeveloperForm.name)
    await message.answer('Enter your fullname:')


@dp.message(DeveloperForm.name, F.text)
async def developer_name_handler(message: Message, state: FSMContext):
    developer_name = message.text
    await state.update_data({'name': developer_name})
    await state.set_state(DeveloperForm.contact)
    await message.answer(text='Share your contact by clicking Contact button', reply_markup=rkb_with_contact())


@dp.message(DeveloperForm.contact, F.contact)
async def developer_contact_handler(message: Message, state: FSMContext):
    developer_contact = message.contact.phone_number
    await state.update_data({'contact': developer_contact})
    await state.set_state(DeveloperForm.occupation)
    await message.answer(text='What is your occupation?', reply_markup=occupation_markup)


@dp.message(DeveloperForm.occupation, F.text)
async def occupation_handler(message: Message, state: FSMContext):
    developer_occupation = message.text
    await state.update_data({'occupation': developer_occupation})
    await state.set_state(DeveloperForm.main_panel)
    data = await state.get_data()
    developer = Developer(chat_id=message.from_user.id,
                          name=data['name'], contact=data['contact'], occupation=data['occupation'])
    developer.save()
    buttons = ['Latest Orders', 'My Orders', 'About Me', 'Settings', 'Contact us', '⬅️Back', 'Back To Register']
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('Welcome To Main Panel', reply_markup=markup)

@dp.message(DeveloperForm.contact, DeveloperForm.occupation, DeveloperForm.main_panel,
            F.text == 'Back To Register')
async def back(message: Message, state: FSMContext):
    await state.clear()
    buttons = ['Developer', 'Customer']
    sizes = [2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('xayr', reply_markup=markup)