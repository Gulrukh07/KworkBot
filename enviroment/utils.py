from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Bot:
    TOKEN = getenv("TOKEN")

class DB:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_NAME")
    DB_PASSWORD = getenv("DB_NAME")
    DB_HOST = getenv("DB_NAME")
    DB_PORT = getenv("DB_NAME")

class Web:
    TOKEN = getenv("WEB_TOKEN")

class Payment:
    CLICK_TOKEN = getenv("CLICK_TOKEN")

class Env:
    bot = Bot()
    db = DB()
    web = Web()
    pay = Payment()