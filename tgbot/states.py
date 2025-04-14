from aiogram.fsm.state import StatesGroup, State


class CustomerForm(StatesGroup):
    name = State()
    contact = State()
    roll = State()
    main_panel = State()

class DeveloperForm(StatesGroup):
    name = State()
    contact = State()
    occupation = State()
    main_panel = State()

class ProjectForm(StatesGroup):
    name = State()
    description = State()
    price = State()
    due_date = State()
    tz_file = State()
    occupation_type = State()
    send_admin = State()
