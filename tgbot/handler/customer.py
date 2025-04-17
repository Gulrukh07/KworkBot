from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import Customer
from tgbot.buttons.reply import rkb_with_contact, make_reply_button, back_markup
from tgbot.buttons.inline import admin_contact
from tgbot.states import CustomerForm, ProjectForm
from .handlers import dp


@dp.message(CustomerForm.settings, F.text == '⬅️Back')
@dp.message(CustomerForm.about_me, F.text == '⬅️Back')
@dp.message(CustomerForm.contact, F.text == '⬅️Back')  # noqa
@dp.message(F.text == "Customer")
async def customer_button_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    c = Customer(user_id=user_id).first()
    if not c:
        await state.set_state(CustomerForm.name)
        await message.answer('Enter your fullname:')
    else:
        await state.set_state(CustomerForm.main_panel)
        buttons = ['Order now', 'My Orders', 'About Me', 'Settings', 'Contact us', 'Back To Register']
        sizes = [1, 2, 2, 2]
        markup = make_reply_button(buttons, sizes)
        await message.answer('Welcome To Main Panel', reply_markup=markup)


@dp.message(CustomerForm.name, F.text.isalpha())
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
    customer_id = message.from_user.id
    customer = Customer(user_id=customer_id, name=data['name'], contact=data['contact'])
    customer.save()
    await state.set_state(CustomerForm.main_panel)
    buttons = ['Order now', 'My Orders', 'About Me', 'Settings', 'Contact us', 'Bact To Register']
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('Welcome To Main Panel', reply_markup=markup)


@dp.message(F.text == 'Order now')
async def order_now_handler(message: Message, state: FSMContext):
    await state.set_state(ProjectForm.name)
    await message.answer(text='Please provide all the information about your project!')
    await message.answer(text='Project name:', reply_markup=back_markup)


@dp.message(CustomerForm.main_panel, F.text == 'About Me')
async def about_me_handler(message: Message, state: FSMContext):
    user = Customer(user_id=message.from_user.id).first()
    await state.set_state(CustomerForm.about_me)
    if user:
        about_me = (
            f" Name: {user.name}\n"
            f" Contact: {user.contact}\n"
        )
    else:
        about_me = 'No Information Found!'
    await message.answer(text=about_me, reply_markup=back_markup)


@dp.message(CustomerForm.main_panel, F.text == 'Settings')
async def about_me_settings_handler(message: Message, state: FSMContext):
    user = Customer(user_id=message.from_user.id).first()
    await state.set_state(CustomerForm.settings)
    await message.answer(text='You can change your information here!')
    if user:
        buttons = ['Name', 'Contact', '⬅️Back']
        sizes = [2,1]
        markup = make_reply_button(buttons, sizes)
        await message.answer(text='What do you want to change?', reply_markup=markup)
    else:
        await message.answer(text='No Information Found!', reply_markup=back_markup)


@dp.message(CustomerForm.settings, F.text.in_({'Name', 'Contact'}))
async def update_user(message: Message):
    if message.text == 'Name':
        await message.answer(text='Please enter your new name!', reply_markup=back_markup)
    elif message.text == 'Contact':
        await message.answer(text='Please enter your new contact!', reply_markup=back_markup)


@dp.message(CustomerForm.settings, F.text.isalpha())
async def update_name(message: Message):
    user = Customer(user_id=message.from_user.id).first()
    user.update(name=message.text)
    await message.answer(text='Your name has been updated!', reply_markup=back_markup)


@dp.message(CustomerForm.settings, F.text.isdigit())
async def update_contact(message: Message):
    user = Customer(user_id=message.from_user.id).first()
    user.update(name=message.text)
    await message.answer(text='Your contact has been updated!', reply_markup=back_markup)

@dp.message(CustomerForm.main_panel, F.text == 'Contact us')
async def contact_us(message:Message):
    await message.answer(text='You can contact to the admin by telegram only!', reply_markup=admin_contact())


