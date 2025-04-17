from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import Customer
from tgbot.buttons.reply import rkb_with_contact, make_reply_button, back_markup
from tgbot.states import CustomerForm, ProjectForm
from .handlers import dp

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


@dp.message(F.text == 'My Orders')
async def my_orders(message: Message):
    ...


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
