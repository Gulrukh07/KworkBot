from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.model import Project
from tgbot.buttons.inline import make_inline_button
from tgbot.buttons.reply import back_markup
from tgbot.dispatcher import dp
from tgbot.handler import admin_id
from tgbot.states import ProjectForm


@dp.message(ProjectForm.occupation_type, F.text)
async def occupation_type_handler(message: Message, state: FSMContext):
    occupation_type = message.text
    await state.update_data(occupation_type=occupation_type)
    ikb_buttons = ['Yes', 'No']
    sizes = [2]
    ikb = make_inline_button(ikb_buttons, sizes, message.from_user.id)
    data = await state.get_data()
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
