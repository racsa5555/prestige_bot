from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    phone_number = State()
    name = State()
    city = State()
    full_name = State()
    id = 0
    update = False

class Calculator(StatesGroup):
    width = State()
    height = State()
    length = State()
    weight = State()