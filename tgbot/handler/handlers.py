from aiogram import Dispatcher
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import User
from tgbot.buttons.reply import make_reply_button, rkb_with_contact
# from tgbot.handler import
from tgbot.states import DeveloperForm, CustomerForm

dp = Dispatcher()

btns = ['⬅️Back']
size = [1]
back_markup = make_reply_button(btns, size)

# @dp.message(CustomerForm.main_panel, F.text == 'Main Menu')
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    buttons = ['Developer', 'Customer']
    sizes = [2]
    markup = make_reply_button(buttons, sizes)
    user = User(chat_id=message.from_user.id).first()
    await state.set_state(CustomerForm.main_panel)
    if user:
        if user.role == 'Customer':
            await state.set_state(CustomerForm.main_panel)
            buttons = ['Order now', 'My Orders', 'About Me', 'Settings', 'Contact us', '⬅️Back', 'Main Menu']
        else:
            await state.set_state(DeveloperForm.main_panel)
            buttons = ['Latest orders', 'My Orders', 'About Me', 'Settings', 'Contact us', '⬅️Back', 'Main Menu']
        sizes = [1, 2, 2, 2]
        markup = make_reply_button(buttons, sizes)
        await message.answer('Welcome To Main Panel', reply_markup=markup)
    else:
        await message.answer(f"Hello, {message.from_user.full_name}!")
        await message.answer(f"Who are You?", reply_markup=markup)


@dp.message(CustomerForm.main_panel, F.text == "Customer")
async def customer_button_handler(message: Message, state: FSMContext) -> None:
    role = message.text
    await state.update_data({'role': role})
    await state.set_state(CustomerForm.name)
    await message.answer('Enter your fullname:', reply_markup=back_markup)


@dp.message(CustomerForm.name, F.text)
async def customer_name_handler(message: Message, state: FSMContext):
    developer_name = message.text
    await state.update_data({'name': developer_name})
    await state.set_state(DeveloperForm.contact)
    await message.answer(text='Share your contact by clicking Contact button', reply_markup=rkb_with_contact())


@dp.message(DeveloperForm.main_panel, F.text == '⬅️Back')
@dp.message(CustomerForm.contact, F.text)
async def customer_contact_handler(message: Message, state: FSMContext):
    developer_contact = message.contact.phone_number
    await state.update_data({'contact': developer_contact})
    data = await state.get_data()
    customer = User(chat_id=message.from_user.id, name=data['name'], contact=data['contact'], role=data['role'])
    customer.save()
    await state.set_state(DeveloperForm.main_panel)
    buttons = ['Order now', 'My Orders', 'About Me', 'Settings', 'Contact us', '⬅️Back', 'Main Menu']
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('Welcome To Main Panel', reply_markup=markup)
