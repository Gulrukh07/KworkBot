from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from db.model import Developer, Project
from tgbot.buttons.inline import admin_contact
from tgbot.buttons.reply import rkb_with_contact, occupation_markup, make_reply_button, back_markup
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm


@dp.message(DeveloperForm.main_panel, F.text == __('⬅️Back'))
@dp.message(DeveloperForm.settings, F.text == __('⬅️Back'))
@dp.message(DeveloperForm.about_me, F.text == __('⬅️Back'))
@dp.message(DeveloperForm.occupation, F.text == __('⬅️Back'))
@dp.message(DeveloperForm.contact, F.text == __('⬅️Back'))
@dp.message(F.text == __('Developer'))
async def developer_button_handler(message: Message, state: FSMContext) -> None:
    user_id = str(message.from_user.id)
    c = Developer(user_id=user_id).first() # noqa
    if not c:
        await state.set_state(DeveloperForm.name)
        await message.answer(_('Enter your fullname:'))
    else:
        await state.set_state(DeveloperForm.main_panel)
        buttons = (_('Latest Orders'), _('My Orders'), _('About Me'),
                   _('Settings'), _('Contact us'), _('Back To Register'))
        sizes = [1, 2, 2, 2]
        markup = make_reply_button(buttons, sizes)
        await message.answer(_('Welcome To Main Panel'), reply_markup=markup)


@dp.message(DeveloperForm.name, F.text)
async def developer_name_handler(message: Message, state: FSMContext):
    developer_name = message.text
    await state.update_data({'name': developer_name})
    await state.set_state(DeveloperForm.contact)
    await message.answer(text=_('Share your contact by clicking Contact button'), reply_markup=rkb_with_contact())


@dp.message(DeveloperForm.contact, F.contact)
async def developer_contact_handler(message: Message, state: FSMContext):
    developer_contact = message.contact.phone_number
    await state.update_data({'contact': developer_contact})
    await state.set_state(DeveloperForm.occupation)
    await message.answer(text=_('What is your occupation?'), reply_markup=occupation_markup)


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
    buttons = (_('Latest Orders'), _('My Orders'), _('About Me'),
               _('Settings'), _('Contact us'), _('Back To Register'))
    sizes = [1, 2, 2, 2]
    markup = make_reply_button(buttons, sizes)
    await message.answer(_('Welcome To Main Panel'), reply_markup=markup)


@dp.message(DeveloperForm.main_panel, F.text == __('About Me'))
async def about_me_handler(message: Message, state: FSMContext):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    await state.set_state(DeveloperForm.about_me)
    if user:
        about_me = _(
            "Name: {name}\nContact: {contact}\nOccupation: {occupation}"
        ).format(name=user.name, contact=user.contact, occupation=user.occupation)
    else:
        about_me = _('No Information Found!')
    await message.answer(text=about_me, reply_markup=back_markup)


@dp.message(DeveloperForm.main_panel, F.text == __('Settings'))
async def about_me_settings_handler(message: Message, state: FSMContext):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    await state.set_state(DeveloperForm.settings)
    await message.answer(text=_('You can change your information here!'))
    if user:
        buttons = _('Name'), _('Contact'), _('Occupation'), _('⬅️Back')
        sizes = [2, 2, 1]
        markup = make_reply_button(buttons, sizes)
        await message.answer(text=_('What do you want to change?'), reply_markup=markup)
    else:
        await message.answer(text=_('No Information Found!'), reply_markup=back_markup)


@dp.message(DeveloperForm.settings, F.text.in_({_('Name'), _('Contact'), _('Occupation')}))
async def update_user(message: Message):
    if message.text == __('Name'):
        await message.answer(text=_('Please enter your new name!'), reply_markup=back_markup)
    elif message.text == __('Contact'):
        await message.answer(text=_('Please enter your new contact!'), reply_markup=back_markup)
    elif message.text == __('Occupation'):
        await message.answer(text=_('Please choose your new occupation!'), reply_markup=occupation_markup)


@dp.message(DeveloperForm.settings, F.text.in_({_('Fullstack'), _('Android'),
                                                _('BackEnd'), _('FrontEnd')}))
async def update_occupation(message: Message):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    user.update(occupation=message.text)
    await message.answer(text=_('Your occupation has been updated!'), reply_markup=back_markup)


@dp.message(DeveloperForm.settings, F.text.isalpha())
async def update_name(message: Message):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    user.update(name=message.text)
    await message.answer(text=_('Your name has been updated!'), reply_markup=back_markup)


@dp.message(DeveloperForm.settings, F.text.isdigit())
async def update_contact(message: Message):
    user = Developer(user_id=str(message.from_user.id)).first() # noqa
    user.update(name=message.text)
    await message.answer(text=_('Your contact has been updated!'), reply_markup=back_markup)

@dp.message(DeveloperForm.main_panel, F.text == __('Contact us'))
async def contact_us(message:Message):
    await message.answer(text=_('You can contact to the admin by telegram only!'), reply_markup=admin_contact())


@dp.message(DeveloperForm.main_panel, F.text == __('My Orders'))
async def my_orders_handler(message:Message):
    projects = Project(developer_id=str(message.from_user.id)).get_all() # noqa
    data = []
    i = 1
    for project in projects:
        data.append(
            _("""Your {i} - Project: \n\n
            📌 Name: {name}\n
            📝 Description: {description}\n
            💰 Price: {price}\n
            📅 Due Date: {due_date}\n
            📂 Tz file: {'tz_file}\n
            🔧 Occupation Type: {occupation_type}\n""").format(i=i,name=project['name'], description = project['description'],
                                                              price=project['price'], due_date=project['due_date'],
                                                              tz_file=project['tz_file'], occupation=project['occupation'])
        )
        i += 1
    formatted_data = "\n" + "\n".join(data)
    await message.answer(text=_('Your Projects:{}').format(formatted_data), reply_markup=back_markup)

@dp.message(DeveloperForm.main_panel, F.text == __('Latest Orders'))
async def latest_orders(message: Message):
    developer_occupation = Developer(user_id=str(message.from_user.id)).first().occupation
    projects = Project(occupation_type=developer_occupation).get_all()
    data = []

    for p in projects[::-1]:
        if p['developer_id']:
            continue

        project_info = _(
            """🆕 Latest Orders: \n\n
            📌 Name: {name}\n
            📝 Description: {description}\n
            💰 Price: {price}\n
            📅 Deadline: {due_date}\n
            📂 Tz file: {tz_file}\n
            🔧 Occupation type: {occupation_type}\n"""
        ).format(
            name=p['name'],
            description=p['description'],
            price=p['price'],
            due_date=p['due_date'],
            tz_file=p['tz_file'],
            occupation_type=p['occupation_type']
        )
        data.append(project_info)
        break

    await message.answer(
        text=data[0] if data else _('No Information Found!'),
        reply_markup=back_markup
    )
