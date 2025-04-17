from pprint import pprint

from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.model import Project
from enviroment.utils import Env
from tgbot.buttons.inline import make_inline_button
from tgbot.buttons.reply import back_markup, occupation_markup
from tgbot.dispatcher import dp
from tgbot.states import ProjectForm, CustomerForm

admin_id = Env().bot.ADMIN


@dp.message(ProjectForm.occupation_type, F.text == '⬅️Back')
@dp.message(ProjectForm.description, F.text == '⬅️Back')
@dp.message(ProjectForm.tz_file, F.text == '⬅️Back')
@dp.message(ProjectForm.due_date, F.text == '⬅️Back')
@dp.message(ProjectForm.price, F.text == '⬅️Back')
@dp.message(CustomerForm.main_panel, F.text == 'Order now')
async def order_now_handler(message: Message, state: FSMContext):
    await state.set_state(ProjectForm.name)
    await message.answer(text='Please provide all the information about your project!')
    await message.answer(text='Project name:', reply_markup=back_markup)


@dp.message(ProjectForm.name, F.text)
async def project_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(ProjectForm.description)
    await message.answer(text='Project Description:', reply_markup=back_markup)


@dp.message(ProjectForm.description, F.text)
async def project_description_handler(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await state.set_state(ProjectForm.price)
    await message.answer(text='How much will you pay?', reply_markup=back_markup)


@dp.message(ProjectForm.price, F.text.isdigit())
async def price_handler(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await state.set_state(ProjectForm.due_date)
    await message.answer(text='Due Date of your project:[YYYY-MM-DD]', reply_markup=back_markup)


@dp.message(ProjectForm.due_date, F.text)
async def due_date_handler(message: Message, state: FSMContext):
    due_date = message.text
    await state.update_data(due_date=due_date)
    await state.set_state(ProjectForm.tz_file)
    await message.answer(text='Do you have TZ file of your Project?[Yes/No]', reply_markup=back_markup)


@dp.message(ProjectForm.tz_file, F.text)
async def tz_file_handler(message: Message, state: FSMContext):
    tz_file = message.text
    await state.update_data(tz_file=tz_file)
    await state.set_state(ProjectForm.occupation_type)
    await message.answer(text='For Whom is Your Project', reply_markup=occupation_markup)

