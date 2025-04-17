from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import Developer
from tgbot.buttons.reply import rkb_with_contact, occupation_markup, make_reply_button, back_markup
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm

@dp.message(DeveloperForm.about_me, F.text == '⬅️Back')
@dp.message(DeveloperForm.occupation, F.text == '⬅️Back')
@dp.message(DeveloperForm.contact, F.text == '⬅️Back')
@dp.message(F.text == 'Developer')
async def developer_button_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    c = Developer(user_id=user_id).first()
    if not c:
        await state.set_state(DeveloperForm.name)
        await message.answer('Enter your fullname:')
    else:
        await state.set_state(DeveloperForm.main_panel)
        buttons = ['Latest Orders', 'My Orders', 'About Me', 'Settings', 'Contact us',  'Back To Register']
        sizes = [1, 2, 2, 2]
        markup = make_reply_button(buttons, sizes)
        await message.answer('Welcome To Main Panel', reply_markup=markup)


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
    developer = Developer(user_id=message.from_user.id,
                          name=data['name'], contact=data['contact'], occupation=data['occupation'])
    developer.save()
    buttons = ['Latest Orders', 'My Orders', 'About Me', 'Settings', 'Contact us', 'Back To Register']
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('Welcome To Main Panel', reply_markup=markup)


@dp.message(DeveloperForm.main_panel, F.text == 'About Me')
async def about_me_handler(message: Message, state: FSMContext):
    user = Developer(user_id=message.from_user.id).first()
    await state.set_state(DeveloperForm.about_me)
    if user:
        about_me = (
            f" Name: {user.name}\n"
            f" Contact: {user.contact}\n"
            f" Occupation: {user.occupation}\n"
        )
    else:
        about_me = 'No Information Found!'
    await message.answer(text=about_me, reply_markup=back_markup)
