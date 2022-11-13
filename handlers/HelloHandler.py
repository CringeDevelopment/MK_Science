from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re 
import asyncio
from config import ADMIN_ID, Directions
from aiogram.dispatcher.filters import Text

''' KEYBOARDS '''
Ybutton = KeyboardButton('Да')
Nbutton = KeyboardButton('Нет')
YNkb = ReplyKeyboardMarkup(resize_keyboard=True).row(Ybutton, Nbutton)

async def KeyboardGeneration(Directions):
	DynamicKeyboard = ReplyKeyboardMarkup(resize_keyboard = True)
	if len(Directions) != 0:
		for i in Directions:
			DynamicKeyboard.add(KeyboardButton(i))
	DynamicKeyboard.add(KeyboardButton('/назад'))
	return DynamicKeyboard



''' STATES '''
class ScienceWork(StatesGroup):
	Direction = State()
	Theme = State()
	Faculty = State()
	FIO = State()
	Description = State()

''' ASYNC MAIN FUNCTIONS '''
async def Welcome(message: types.Message):
	await message.answer(f'Привет, {message.from_user.full_name}, хочешь написать научную статью?', reply_markup=YNkb )#ADD REPLY MARKUP

async def GoodBoy(message: types.Message):
	keyboard = await KeyboardGeneration(Directions)
	await message.answer(f'Выбери свое направление', reply_markup=keyboard)
	await ScienceWork.Direction.set()

async def NotGoodBoy(message: types.Message):
	await message.answer(f'Удачи!')

async def UploadDirection(message : types.Message, state : FSMContext):
	await state.update_data(direct = message.text)
	await message.answer(f'Выбери свою тему')
	await ScienceWork.next()

async def UploadTheme(message : types.Message, state : FSMContext):
	await state.update_data(them = message.text)
	await message.answer(f'Выбери свой факультет')
	await ScienceWork.next()

async def UploadFaculty(message : types.Message, state : FSMContext):
	await state.update_data(facult = message.text)
	await message.answer(f'Введи ФИО')
	await ScienceWork.next()

async def UploadFIO(message : types.Message, state : FSMContext):
	await state.update_data(FIIO = message.text)
	await message.answer(f'Добавь описание')
	await ScienceWork.next()

async def UploadDescription(message : types.Message, state : FSMContext):
	await state.update_data(descript = message.text)
	data = await state.get_data()
	await message.answer(f'Ожидайте ответа от админимтратора')
	await bot.send_message(ADMIN_ID, f"""
Есть желающий написать статью!!!
Направление: {data['direct']}, 
Тема: {data['them']},
Факультет: {data['facult']},
ФИО: {data['FIIO']},
Описание: {data['descript']}
""")






''' DECORATOR FOR MESSAGES AND CALLBACK '''
def decorator(dp : Dispatcher):
	dp.register_message_handler(Welcome, commands=['Start'])
	dp.register_message_handler(GoodBoy, Text(startswith='Да'))
	dp.register_message_handler(NotGoodBoy, Text(startswith='Нет'))
	dp.register_message_handler(UploadDirection, state = ScienceWork.Direction)
	dp.register_message_handler(UploadTheme, state = ScienceWork.Theme)
	dp.register_message_handler(UploadFaculty, state = ScienceWork.Faculty)
	dp.register_message_handler(UploadFIO, state = ScienceWork.FIO)
	dp.register_message_handler(UploadDescription, state = ScienceWork.Description)