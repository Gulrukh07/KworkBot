from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import User
from tgbot.buttons.reply import rkb_with_contact, make_reply_button, back_markup
from tgbot.states import CustomerForm, ProjectForm, DeveloperForm, Start
from .handlers import dp


# @dp.message(DeveloperForm.main_panel, F.text == 'Back to Register')  # noqa
@dp.message(CustomerForm.contact, F.text == '⬅️Back')  # noqa
@dp.message(CustomerForm.start, F.text == "Customer")
async def customer_button_handler(message: Message, state: FSMContext) -> None:
    role = message.text
    await state.update_data({'role': role})
    await state.set_state(CustomerForm.name)
    await message.answer('Enter your fullname:', reply_markup=back_markup)


@dp.message(CustomerForm.main_panel, F.text == '⬅️Back')
@dp.message(CustomerForm.name, F.text)
async def customer_name_handler(message: Message, state: FSMContext):
    customer_name = message.text
    await state.update_data({'name': customer_name})
    await state.set_state(CustomerForm.contact)
    await message.answer(text='Share your contact by clicking Contact button', reply_markup=rkb_with_contact())


@dp.message(CustomerForm.contact, F.contact)
async def customer_contact_handler(message: Message, state: FSMContext):
    customer_contact = message.contact.phone_number
    await state.update_data({'contact': customer_contact})
    data = await state.get_data()
    customer = User(chat_id=message.from_user.id, name=data['name'], contact=data['contact'], role=data['role'])
    customer.save()
    # await state.set_state(CustomerForm)
    buttons = ['Order now', 'My Orders', 'About Me', 'Settings', 'Contact us', '⬅️Back', 'Back To Register']
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('Welcome To Main Panel', reply_markup=markup)


@dp.message(F.text == 'Order now')
async def order_now_handler(message: Message, state: FSMContext):
    await state.set_state(ProjectForm.name)
    await message.answer(text='Please provide all the information about your project!')
    await message.answer(text='Project name:', reply_markup=back_markup)



