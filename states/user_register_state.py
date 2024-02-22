from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    phone_number = State()
    name = State()
    city = State()
    full_name = State()
    id = 0
    update = False
    language = State()

class Track_code(StatesGroup):
    track_code = State()

class Calculator(StatesGroup):
    width = State()
    height = State()
    length = State()
    weight = State()

class Admin(StatesGroup):
    password = State()
    is_admin = False
    set_table = State()