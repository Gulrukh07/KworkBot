from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.model import Project, Developer
from tgbot.buttons.inline import make_inline_button, developer_response, chat_with_developer
from tgbot.buttons.reply import back_markup
from tgbot.dispatcher import dp
from tgbot.handler import admin_id
from tgbot.states import ProjectForm


@dp.message(ProjectForm.occupation_type, F.text)
async def send_admin_handler(message: Message, state: FSMContext):
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
    customer_id = callback.data.split('_')[-1]
    await bot.send_message(chat_id=int(customer_id), text="✅ Project Accepted!")
    await state.clear()
    await callback.message.answer("✅ Project saved successfully!")
    await callback.answer()

    devops = Developer().get_all('user_id')
    project = Project(user_id=int(customer_id)).get_all()[-1]
    project_info = (
        f"📌 Name: {project['name']}\n"
        f"📝 Description: {project['description']}\n"
        f"💰 Price: {project['price']}\n"
        f"📅 Due Date: {project['due_date']}\n"
        f"📂 Tz file: {project['tz_file']}\n"
        f"🔧 Occupation Type: {project['occupation_type']}"
    )
    for d in devops:
        await bot.send_message(chat_id=d['user_id'], text=f"{project_info}", reply_markup=developer_response(d['user_id']))


@dp.callback_query(F.data.startswith('No'))
async def cancel_project(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split('_')[-1])
    project = Project(user_id=user_id).first()
    project.delete()
    await state.clear()
    await callback.message.answer("❌ Project Rejected.")
    await callback.answer()

@dp.callback_query(F.data.startswith('Accepted_'))
async def devops_response(callback: CallbackQuery, bot:Bot):
    developer_username = callback.from_user.username
    ikb = chat_with_developer(developer_username)

    deal_buttons = ['Yes']
    sizes = [1]
    deal_ikb = make_inline_button(deal_buttons, sizes, callback.from_user.id)

    customer_id = int(callback.data.split('_')[-1])
    await bot.send_message(chat_id= customer_id,text=f"✅ Your Project is Accepted by Developer")
    await bot.send_message(chat_id= customer_id,text=f"You can chat with Developer",reply_markup=ikb)
    await bot.send_message(chat_id= customer_id,text=f"Have a deal with Developer?",reply_markup=deal_ikb)
    await bot.send_message(chat_id= admin_id,text=f"Project is Accepted by {developer_username}")
    await callback.answer()


@dp.callback_query(F.data.startswith('Yes_'))
async def customer_response(callback: CallbackQuery, bot:Bot):
    customer_id = callback.from_user.id
    project = Project(user_id=customer_id).get_all()[-1]
    project_id = project['id']
    await bot.send_message(chat_id=admin_id, text=f'{project_id} by {customer_id} agreed with developer {developer_id}')
    await callback.answer()
