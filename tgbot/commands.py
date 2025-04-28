from aiogram import Bot
from aiogram.types import BotCommand


async def on_startup(bot: Bot) -> None:
    bot_commands = [
        BotCommand(command="start", description="boshlash"),
        BotCommand(command="change_language", description="tilni almashtirish")
    ]
    await bot.set_my_commands(bot_commands)
