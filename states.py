from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStatesGroup(StatesGroup):
    full_name = State()
    contact = State()
    submitting = State()

