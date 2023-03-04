import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.types import Message
from goods import find_goods
from dotenv import load_dotenv

# инициализация объекта драйвера
# DRIVER_PATH = os.path.join(os.getcwd(), 'fptr10.dll')
# fptr = IFptr(DRIVER_PATH)
load_dotenv()
BOT_ID = os.getenv('BOT_ID')

logging.basicConfig(level=logging.INFO)
# Объект бота

# Диспетчер
dp = Dispatcher()
logger = logging.getLogger(__name__)


# Хэндлер на команду /start
@dp.message()
async def echo_message(msg: Message):
    await find_goods(msg)
# Запуск процесса поллинга новых апдейтов
def main():
    bot = Bot(BOT_ID, parse_mode="HTML")
    dp.run_polling(bot)

if __name__ == "__main__":
    main()