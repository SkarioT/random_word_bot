from . API_KEY import POLSKI_RANDOM_BOT_TOKEN
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(POLSKI_RANDOM_BOT_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())

