from aiogram.fsm.state import StatesGroup, State


class CustomerForm(StatesGroup):
    name = State()
    contact = State()
    main_panel = State()
    about_me = State()
    settings = State()
    my_orders = State()
    contact_us = State()


class DeveloperForm(StatesGroup):
    name = State()
    contact = State()
    occupation = State()
    main_panel = State()
    about_me = State()
    settings = State()
    my_orders = State()
    contact_us = State()


class ProjectForm(StatesGroup):
    name = State()
    description = State()
    price = State()
    due_date = State()
    tz_file = State()
    occupation_type = State()
