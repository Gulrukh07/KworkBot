from aiogram.fsm.state import StatesGroup, State


class CustomerForm(StatesGroup):
    name = State()
    contact = State()
    main_panel = State()
    about_me = State()
    settings = State()

class DeveloperForm(StatesGroup):
    name = State()
    contact = State()
    occupation = State()
    main_panel = State()
    about_me = State()
    settings = State()


class ProjectForm(StatesGroup):
    name = State()
    description = State()
    price = State()
    due_date = State()
    tz_file = State()
    occupation_type = State()
    tz_file_exist = State()

class BotState(StatesGroup):
    language = State()