import logging

import requests, os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from goods import find_goods
from orders import main_choice

load_dotenv()
BOT_ID = os.getenv('BOT_ID')
CASH_URL = os.getenv('CASH_URL')

# Задаем уровень логов
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=BOT_ID)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    search_goods = State()
    search_orders = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.reply("Привет! Я бот для работы с вашим бизнесом.")


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: Message):
    await message.reply("Я могу помочь вам в работе с бизнесом. Вот что я умею:\n"
                        "/goods - поиск товаров\n"
                        "/cash - данные кассы\n"
                        "/orders - поиск заказов\n"
                        "/helpdesk - техническая поддержка\n"
                        "/portal - доступ к порталу")


# Обработчик команды /cash
@dp.message_handler(commands=['cash'])
async def cmd_cash(message: Message):
    # Здесь мы посылаем запрос на API server и получаем данные
    response = requests.get(CASH_URL)
    try:
        if response.status_code == 200:
            data = response.json()
            cash_info = data.get("cash_info", {})
            cashsum = data.get("cashsum", "")
            sum_in = data.get("sum_in", "")
            sum_out = data.get("sum_out", "")
            revenue = data.get("revenue", "")

            # Отправляем сообщение с полученными данными
            await message.answer(f"Статус кассы: {cash_info['status']}\n"
                                f"time: {cash_info['time']}\n"
                                f"непереданные: {cash_info['not_trans']}\n"
                                f"Денег в кассе: {cashsum}\n"
                                f"внесения: {sum_in}\n"
                                f"выплаты: {sum_out}\n"
                                f"выручка: {revenue}")
        else:
            await message.answer("Ошибка получения данных из API сервера")
    except Exception as e:
            await message.answer("Ошибка получения данных из API сервера")

# Обработчик команды /goods
@dp.message_handler(commands=['goods'])
async def cmd_goods(message: types.Message):
    
    await Form.search_goods.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("cancel")
    await message.reply("Введите фразу для поиска товаров:", reply_markup=markup)

# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())



@dp.message_handler(state=Form.search_goods)
async def process_search(message: types.Message, state: FSMContext):
    """
    Process user search
    """
    async with state.proxy() as data:
        data['name'] = message.text
    
    await find_goods(message)

# Обработчик команды /orders
@dp.message_handler(commands=['orders'])
async def cmd_orders(message: Message):
        
    await Form.search_orders.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("за день", "cancel")
    await message.reply("Введите фразу для поиска заказов:", reply_markup=markup)
    
@dp.message_handler(state=Form.search_orders)
async def process_search(message: types.Message, state: FSMContext):
    """
    Process user search
    """
    async with state.proxy() as data:
        data['name'] = message.text
    try:
        orders = main_choice(message.text)
        await message.answer(orders, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Ошибка - {e}")



@dp.message_handler(commands=['helpdesk'])
async def cmd_helpdesk(message: Message):
	await message.answer("Свяжитесь с нами по телефону 8-918-0-444-262")

@dp.message_handler(commands=['portal'])
async def cmd_portal(message: Message):
	await message.answer("Перейдите по ссылке http://mu.com.ru")

executor.start_polling(dp, skip_updates=True)
 