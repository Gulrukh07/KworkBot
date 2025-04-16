from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.model import Project
from enviroment.utils import Env
from tgbot.buttons.inline import make_inline_button
from tgbot.buttons.reply import back_markup, occupation_markup, make_reply_button
from tgbot.dispatcher import dp
from tgbot.states import ProjectForm

admin_id = Env().bot.ADMIN


@dp.message(ProjectForm.occupation_type, F.text == '⬅️Back')
@dp.message(ProjectForm.tz_file, F.text == '⬅️Back')
@dp.message(ProjectForm.due_date, F.text == '⬅️Back')
@dp.message(ProjectForm.price, F.text == '⬅️Back')
@dp.message(ProjectForm.name, F.text)
async def project_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data({'name': name})
    await state.set_state(ProjectForm.description)
    await message.answer(text='Project Description:', reply_markup=back_markup)


@dp.message(ProjectForm.description, F.text)
async def project_description_handler(message: Message, state: FSMContext):
    description = message.text
    await state.update_data({'description': description})
    await state.set_state(ProjectForm.price)
    await message.answer(text='How much will you pay?', reply_markup=back_markup)


@dp.message(ProjectForm.price, F.text.isdigit())
async def price_handler(message: Message, state: FSMContext):
    price = message.text
    await state.update_data({'price': price})
    await state.set_state(ProjectForm.due_date)
    await message.answer(text='Due Date of your project:[YYYY-MM-DD]', reply_markup=back_markup)


@dp.message(ProjectForm.due_date, F.text)
async def due_date_handler(message: Message, state: FSMContext):
    due_date = message.text
    print(due_date)
    print(type(due_date))
    await state.update_data({'due_date': due_date})
    await state.set_state(ProjectForm.tz_file)
    await message.answer(text='Do you have TZ file of your Project?[Yes/No]', reply_markup=back_markup)


@dp.message(ProjectForm.send_admin, F.text == '⬅️Back')
@dp.message(ProjectForm.tz_file, F.text)
async def tz_file_handler(message: Message, state: FSMContext):
    tz_file = message.text
    await state.update_data({'tz_file': tz_file})
    await state.set_state(ProjectForm.occupation_type)
    await message.answer(text='For Whom is Your Project', reply_markup=occupation_markup)


@dp.message(ProjectForm.occupation_type, F.text)
async def occupation_type_handler(message: Message, state: FSMContext):
    occupation_type = message.text
    await state.update_data({'occupation_type': occupation_type})
    await state.set_state(ProjectForm.send_admin)
    data = await state.get_data()
    project = Project(name=data['name'], description=data['description'], price=data['price'],
                      due_date=data['due_date'], tz_file=data['tz_file'], occupation_type=data['occupation_type'])
    project.save()
    buttons = ['⬅️Back', 'Back to Register']
    sizes = [1]
    markup = make_reply_button(buttons, sizes)
    await message.answer(text='Your order is sent to the Admin\nPlease,wait the Confirmation!!', reply_markup=markup)
    ikb_buttons = ['Yes', 'No']
    sizes = [2]
    ikb = make_inline_button(ikb_buttons, sizes)
    await message.bot.send_message(chat_id=admin_id,
                                   text=f"<b>New project received:</b>\n\n"
                                        f"📌 Name: {project.name}\n"
                                        f"📝 Description: {project.description}\n"
                                        f"💰 Price: {project.price}\n"
                                        f"📅 Due Date: {project.due_date}\n"
                                        f"📂 Tz file: {project.tz_file}\n"
                                        f"🔧 Occupation Type: {project.occupation_type}",
                                   reply_markup=ikb)


@dp.callback_query(F.data.in_({'Yes', 'No'}))
async def admin_response_handler(callback: CallbackQuery, state: FSMContext):
    project = Project()
    project.first()
    admin_response = callback.data
    ikb_buttons = ['Receive']
    sizes = [1]
    ikb = make_inline_button(ikb_buttons, sizes)
    if admin_response == 'Yes':
        await callback.answer(text='Congrats, Your order is confirmed 🥳')
        await callback.bot.send_message(chat_id=7397002358, text=f"📌 Project Name:{project.name}\n"
                                                                 f"📝 Project Description:{project.description}\n"
                                                                 f"💰 Project Price:{project.price}\n"
                                                                 f"📅 Project Due Data:{project.due_date}\n"
                                                                 f"📂 Project Tz file:{project.tz_file}\n"
                                                                 f"🔧 Project Occupation Type:{project.occupation_type}\n",
                                        reply_markup=ikb)
    elif admin_response == 'No':
        await callback.answer(text='Sorry, Your order is rejected 😭')
