import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from enviroment.utils import Env
from tgbot.commands import on_startup
from tgbot.handler.handlers import dp
from tgbot.handler.language import router_language

TOKEN = Env().bot.TOKEN


async def main() -> None:
    i18n = I18n(path="locales", default_locale='en')
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(on_startup)
    dp.include_router(router_language)
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n=i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
