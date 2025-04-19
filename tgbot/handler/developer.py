from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.model import Developer, Project
from tgbot.buttons.inline import admin_contact
from tgbot.buttons.reply import rkb_with_contact, occupation_markup, make_reply_button, back_markup
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm


@dp.message(DeveloperForm.main_panel, F.text == '⬅️Back')
@dp.message(DeveloperForm.settings, F.text == '⬅️Back')
@dp.message(DeveloperForm.about_me, F.text == '⬅️Back')
@dp.message(DeveloperForm.occupation, F.text == '⬅️Back')
@dp.message(DeveloperForm.contact, F.text == '⬅️Back')
@dp.message(F.text == 'Developer')
async def developer_button_handler(message: Message, state: FSMContext) -> None:
    user_id = str(message.from_user.id)
    c = Developer(user_id=user_id).first() # noqa
    if not c:
        await state.set_state(DeveloperForm.name)
        await message.answer('Enter your fullname:')
    else:
        await state.set_state(DeveloperForm.main_panel)
        buttons = ['Latest Orders', 'My Orders', 'About Me', 'Settings', 'Contact us', 'Back To Register']
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
    tg_username = message.from_user.username
    await state.update_data({'occupation': developer_occupation})
    await state.set_state(DeveloperForm.main_panel)
    data = await state.get_data()
    developer = Developer(user_id=message.from_user.id,tg_username=tg_username,
                          name=data['name'], contact=data['contact'], occupation=data['occupation'])
    developer.save()
    buttons = ['Latest Orders', 'My Orders', 'About Me', 'Settings', 'Contact us', 'Back To Register']
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer('Welcome To Main Panel', reply_markup=markup)


@dp.message(DeveloperForm.main_panel, F.text == 'About Me')
async def about_me_handler(message: Message, state: FSMContext):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
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


@dp.message(DeveloperForm.main_panel, F.text == 'Settings')
async def about_me_settings_handler(message: Message, state: FSMContext):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    await state.set_state(DeveloperForm.settings)
    await message.answer(text='You can change your information here!')
    if user:
        buttons = ['Name', 'Contact', 'Occupation', '⬅️Back']
        sizes = [2, 2, 1]
        markup = make_reply_button(buttons, sizes)
        await message.answer(text='What do you want to change?', reply_markup=markup)
    else:
        await message.answer(text='No Information Found!', reply_markup=back_markup)


@dp.message(DeveloperForm.settings, F.text.in_({'Name', 'Contact', 'Occupation'}))
async def update_user(message: Message):
    if message.text == 'Name':
        await message.answer(text='Please enter your new name!', reply_markup=back_markup)
    elif message.text == 'Contact':
        await message.answer(text='Please enter your new contact!', reply_markup=back_markup)
    elif message.text == 'Occupation':
        await message.answer(text='Please choose your new occupation!', reply_markup=occupation_markup)


@dp.message(DeveloperForm.settings, F.text.in_({'Fullstack', 'Android', 'BackEnd', 'FrontEnd'}))
async def update_occupation(message: Message):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    user.update(occupation=message.text)
    await message.answer(text='Your occupation has been updated!', reply_markup=back_markup)


@dp.message(DeveloperForm.settings, F.text.isalpha())
async def update_name(message: Message):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    user.update(name=message.text)
    await message.answer(text='Your name has been updated!', reply_markup=back_markup)


@dp.message(DeveloperForm.settings, F.text.isdigit())
async def update_contact(message: Message):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    user.update(name=message.text)
    await message.answer(text='Your contact has been updated!', reply_markup=back_markup)

@dp.message(DeveloperForm.main_panel, F.text == 'Contact us')
async def contact_us(message:Message):
    await message.answer(text='You can contact to the admin by telegram only!', reply_markup=admin_contact())


@dp.message(DeveloperForm.main_panel, F.text == 'My Orders')
async def my_orders_handler(message:Message):
    projects = Project(developer_id=str(message.from_user.id)).get_all() # noqa
    data = []
    i = 1
    for project in projects:
        data.append(
            f"Your {i} - Project: \n\n"
            f"📌 Name: {project['name']}\n"
            f"📝 Description: {project['description']}\n"
            f"💰 Price: {project['price']}\n"
            f"📅 Due Date: {project['due_date']}\n"
            f"📂 Tz file: {project['tz_file']}\n"
            f"🔧 Occupation Type: {project['occupation_type']}\n"
        )
        i+=1
    formatted_data = "\n" + "\n".join(data)
    await message.answer(text=f'Your Projects:{formatted_data}', reply_markup=back_markup)

@dp.message(DeveloperForm.main_panel, F.text == 'Latest Orders')
async def latest_orders(message:Message):
    developer_occupation = Developer(user_id=str(message.from_user.id)).first().occupation # noqa
    project = Project(occupation_type=developer_occupation).get_all()
    data = []
    for p in project[::-1]:
        if p['developer_id'] != None: # noqa
            continue
        else:
            project_info =(
                f"  Latest Order: \n\n"
                f"📌 Name: {p['name']}\n"
                f"📝 Description: {p['description']}\n"
                f"💰 Price: {p['price']}\n"
                f"📅 Due Date: {p['due_date']}\n"
                f"📂 Tz file: {p['tz_file']}\n"
                f"🔧 Occupation Type: {p['occupation_type']}\n"
            )
            data.append(project_info)
            break
    if len(data) != 0:
        await message.answer(text=data[0],reply_markup=back_markup)
    else:
        await message.answer(text='No Information Found!', reply_markup=back_markup)

