from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import lazy_gettext as __, gettext as _

from db.model import Customer, Project
from tgbot.buttons.inline import admin_contact
from tgbot.buttons.reply import rkb_with_contact, make_reply_button, back_markup
from tgbot.states import CustomerForm, ProjectForm
from .handlers import dp


@dp.message(CustomerForm.main_panel, F.text == __('⬅️Back'))
@dp.message(ProjectForm.occupation_type, F.text == __('⬅️Back'))
@dp.message(ProjectForm.description, F.text == __('⬅️Back'))
@dp.message(ProjectForm.tz_file, F.text == __('⬅️Back'))
@dp.message(ProjectForm.due_date, F.text == __('⬅️Back'))
@dp.message(ProjectForm.price, F.text == __('⬅️Back'))
@dp.message(CustomerForm.settings, F.text == __('⬅️Back'))
@dp.message(CustomerForm.about_me, F.text == __('⬅️Back'))
@dp.message(CustomerForm.contact, F.text == __('⬅️Back'))  # noqa
@dp.message(F.text == __("Customer"))
async def customer_button_handler(message: Message, state: FSMContext) -> None:
    user_id = str(message.from_user.id)
    c = Customer(user_id=user_id).first()  # noqa
    if not c:
        await state.set_state(CustomerForm.name)
        await message.answer(_('Enter your fullname:'))
    else:
        await state.set_state(CustomerForm.main_panel)
        buttons = (_('Order now'), _('My Orders'), _('About Me'),
                   _('Settings'), _("Contact us"), _('Back To Register'))
        sizes = [1, 2, 2, 2]
        markup = make_reply_button(buttons, sizes)
        await message.answer(_('Welcome To Main Panel'), reply_markup=markup)


@dp.message(CustomerForm.name, F.text.isalpha())
async def customer_name_handler(message: Message, state: FSMContext):
    customer_name = message.text
    await state.update_data({'name': customer_name})
    await state.set_state(CustomerForm.contact)
    await message.answer(text=_('Share your contact by clicking Contact button'), reply_markup=rkb_with_contact())


@dp.message(CustomerForm.contact, F.contact)
async def customer_contact_handler(message: Message, state: FSMContext):
    customer_contact = message.contact.phone_number
    await state.update_data({'contact': customer_contact})
    data = await state.get_data()
    customer_id = message.from_user.id
    customer = Customer(user_id=customer_id, name=data['name'], contact=data['contact'])
    customer.save()
    await state.set_state(CustomerForm.main_panel)
    sizes = [1, 2, 2, 2]
    buttons = (_('Order now'), _('My Orders'), _('About Me'),
               _('Settings'), _("Contact us"), _('Back To Register'))
    markup = make_reply_button(buttons, sizes)
    await message.answer(_('Welcome To Main Panel'), reply_markup=markup)


@dp.message(CustomerForm.main_panel, F.text == __('About Me'))
async def about_me_handler(message: Message, state: FSMContext):
    user = Customer(user_id=str(message.from_user.id)).first()  # noqa
    await state.set_state(CustomerForm.about_me)
    if user:
        about_me = _(
            "Name: {name}\nContact: {contact}\n"
        ).format(name=user.name, contact=user.contact)

    else:
        about_me = _('No Information Found!')
    await message.answer(text=about_me, reply_markup=back_markup)


@dp.message(CustomerForm.main_panel, F.text == __('Settings'))
async def about_me_settings_handler(message: Message, state: FSMContext):
    user = Customer(user_id=str(message.from_user.id)).first()  # noqa
    await state.set_state(CustomerForm.settings)
    await message.answer(text=_('You can change your information here!'))
    if user:
        buttons = _('Name'), _('Contact'), _('⬅️Back')
        sizes = [2, 1]
        markup = make_reply_button(buttons, sizes)
        await message.answer(text=_('What do you want to change?'), reply_markup=markup)
    else:
        await message.answer(text=_('No Information Found!'), reply_markup=back_markup)


@dp.message(CustomerForm.settings, F.text.in_({_('Name'), _('Contact')}))
async def update_user(message: Message):
    if message.text == __('Name'):
        await message.answer(text=_('Please enter your new name!'), reply_markup=back_markup)
    elif message.text == __('Contact'):
        await message.answer(text=_('Please enter your new contact!'), reply_markup=back_markup)


@dp.message(CustomerForm.settings, F.text.isalpha())
async def update_name(message: Message):
    user = Customer(user_id=str(message.from_user.id)).first()  # noqa
    user.update(name=message.text)
    await message.answer(text=_('Your name has been updated!'), reply_markup=back_markup)


@dp.message(CustomerForm.settings, F.text.isdigit())
async def update_contact(message: Message):
    user = Customer(user_id=str(message.from_user.id)).first()  # noqa
    user.update(name=message.text)
    await message.answer(text=_('Your contact has been updated!'), reply_markup=back_markup)


@dp.message(CustomerForm.main_panel, F.text == __('Contact us'))
async def contact_us(message: Message):
    await message.answer(text=_('You can contact to the admin by telegram only!'), reply_markup=admin_contact())


@dp.message(CustomerForm.main_panel, F.text == __('My Orders'))
async def my_orders_handler(message: Message, state: FSMContext):
    projects = Project(user_id=str(message.from_user.id)).get_all()  # noqa
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
