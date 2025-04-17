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


@dp.message(ProjectForm.occupation_type, F.text)
async def occupation_type_handler(message: Message, state: FSMContext):
    occupation_type = message.text
    await state.update_data(occupation_type=occupation_type)
    ikb_buttons = ['Yes', 'No']
    sizes = [2]
    ikb = make_inline_button(ikb_buttons, sizes, message.from_user.id)
    data = await state.get_data()
    pprint(data)
    await message.bot.send_message(chat_id=admin_id,
                                   text=f"<b>New project received:</b>\n\n"
                                        f"📌 Name: {data['name']}\n"
                                        f"📝 Description: {data['description']}\n"
                                        f"💰 Price: {data['price']}\n"
                                        f"📅 Due Date: {data['due_date']}\n"
                                        f"📂 Tz file: {data['tz_file']}\n"
                                        f"🔧 Occupation Type: {data['occupation_type']}",
                                   reply_markup=ikb)
    await message.answer(text='Your order is sent to the Admin\nPlease,wait the Confirmation!!',
                         reply_markup=back_markup)
    project = Project(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        user_id=int(message.from_user.id),
        due_date=data['due_date'],
        tz_file=data['tz_file'],
        occupation_type=data['occupation_type']
    )
    project.save()


@dp.callback_query(F.data.startswith('Yes_'))
async def message_send_admin(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.data.split('_')[-1]
    await bot.send_message(chat_id=int(user_id), text="✅ Project Accepted!")
    await state.clear()
    await callback.message.answer("✅ Project saved successfully!")
    await callback.answer()


@dp.callback_query(F.data.startswith('No'))
async def cancel_project(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split('_')[-1])
    project = Project(user_id=user_id).first()
    project.delete()
    await state.clear()
    await callback.message.answer("❌ Project submission canceled.")
    await callback.answer()
