# from aiogram.types import Message
#
# from db.model import Project
# from enviroment.utils import Env
# from tgbot.dispatcher import dp
#
# admin_id = Env().bot.ADMIN
#
# from tgbot.buttons.inline import make_inline_button
#
#
# @dp.message()
# async def send_admin(message: Message):
#     ikb_buttons = ['Yes', 'No']
#     sizes = [2]
#     ikb = make_inline_button(ikb_buttons, sizes)
#     project = Project(user_id=message.from_user.id).get_all()[-1]
#     await message.bot.send_message(chat_id=admin_id,
#                                    text=f"<b>New project received:</b>\n\n"
#                                         f"📌 Name: {project.get('name')}\n"
#                                         f"📝 Description: {project.get('description')}\n"
#                                         f"💰 Price: {project.get('price')}\n"
#                                         f"📅 Due Date: {project.get('due_date')}\n"
#                                         f"📂 Tz file: {project.get('tz_file')}\n"
#                                         f"🔧 Occupation Type: {project.get('occupation_type')}",
#                                    reply_markup=ikb)
#
# #
# # @dp.callback_query(F.data.in_({'Yes', 'No'}))
# # async def admin_response_handler(callback: CallbackQuery):
# #     project = Project(user_id=).get_all()[-1]
# #     admin_response = callback.data
# #     ikb_buttons = ['Receive']
# #     sizes = [1]
# #     ikb = make_inline_button(ikb_buttons, sizes)
# #     if admin_response == 'Yes':
# #         await callback.answer(text='Congrats, Your order is confirmed 🥳')
# #         await callback.bot.send_message(chat_id=7397002358, text=f"📌 Project Name:{project.name}\n"
# #                                                                  f"📝 Project Description:{project.description}\n"
# #                                                                  f"💰 Project Price:{project.price}\n"
# #                                                                  f"📅 Project Due Data:{project.due_date}\n"
# #                                                                  f"📂 Project Tz file:{project.tz_file}\n"
# #                                                                  f"🔧 Project Occupation Type:{project.occupation_type}\n",
# #                                         reply_markup=ikb)
# #     elif admin_response == 'No':
# #         await callback.answer(text='Sorry, Your order is rejected 😭')
