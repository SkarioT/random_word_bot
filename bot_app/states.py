from tracemalloc import start
from aiogram.dispatcher.filters.state import State,StatesGroup

class GameStates(StatesGroup):
    default = State()
    start = State()
    random_word = State()