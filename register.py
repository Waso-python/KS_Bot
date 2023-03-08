from bot import db, UserRegister
from aiogram.dispatcher.filters import Command, Text





@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Введите ваше имя:")


# функция-обработчик сообщения с именем пользователя, которая сохраняет имя и переходит на следующее состояние формы
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Введите ваш возраст:")


# функция-обработчик сообщения с возрастом пользователя, которая сохраняет возраст и переходит на следующее состояние формы
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    await message.reply("Пожалуйста, введите число. Введите ваш возраст:")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)

    await Form.next()
    await message.reply("Введите город:")


# функция-обработчик сообщения с городом пользователя, которая сохраняет город и выводит результат заполнения формы
@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
        user_data = {
            'name': data['name'],
            'age': data['age'],
            'city': data['city']
        }
        await message.reply("Спасибо за заполнение формы!\n" + md.text(md.text('Имя:'), md.bold(user_data['name'])) +
                            md.text(md.text('Возраст: