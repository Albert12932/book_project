from engine import *
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_datafactory import EditBookCallbackData
from .get_info import get_all_id, log_add, get_name, get_surname, get_group, get_book_name, get_date
import datetime


add_info_router = Router()

class Add_info(StatesGroup):
    edit_info = State()

async def new_user(message: types.Message):
    if str(message.from_user.id) not in await get_all_id():
        cur.execute(f"insert into people (user_id, username) values ('{message.from_user.id}', '{message.from_user.username}')")
        conn.commit()
        await log_add(message.from_user.id, 'Новый пользователь', datetime.datetime.now())

async def profile_show(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Добавить информацию', callback_data=EditBookCallbackData(command='add_info', book_id='', user_id=f'{message.from_user.id}', group_name=''))
    await message.answer(f"""
➖➖➖➖➖➖➖➖➖➖➖
🔑 Логин: {message.from_user.username}
💳 ID: {message.from_user.id}
{str(f'Имя: <{get_name(str(message.from_user.id))}>') if get_name(str(message.from_user.id)) else ''}
{str(f'Фамилия: <{get_surname(str(message.from_user.id))}>') if get_surname(str(message.from_user.id)) else ''}
{str(f'Группа: <{get_group(str(message.from_user.id))}>') if get_group(str(message.from_user.id)) else ''}
➖➖➖➖➖➖➖➖➖➖➖
""", reply_markup=keyboard.as_markup())
    await log_add(message.from_user.id, 'Профиль', datetime.datetime.now())
    

async def add_info(call: types.CallbackQuery, callback_data: EditBookCallbackData, state: FSMContext):
    await call.message.answer('Введите информацию в формате Иванов_Иван_ШАД-111')
    await state.set_state(Add_info.edit_info)

@add_info_router.message(Add_info.edit_info)
async def edit_info(message: types.Message, state: FSMContext):
    info = message.text.split('_')
    cur.execute(f"update people set surname='{info[0]}', name='{info[1]}', group_name='{info[2]}' where user_id = '{message.from_user.id}'")
    conn.commit()
    await message.answer('Информация успешно добавлена')
    await state.clear()
    await log_add(message.from_user.id, 'Добавить инфу', datetime.datetime.now(), f"info = {info[0]}{info[1]}{info[2]}")

async def help(message: types.Message):
    await message.answer('С вопросами и предложениями обращайтесь к @Albertt1001')
    await log_add(message.from_user.id, 'Помощь', datetime.datetime.now())

async def my_books(message: types.Message):
    cur.execute(f"select book_id from books where holder = '{message.from_user.id}'")
    result = cur.fetchall()
    if len(result) == 0:
        await message.answer('У вас нет книг')
        return
    books = []
    str_books = []
    for i in result:
        books.append(await get_book_name(i[0]))
        str_books.append(f'{await get_book_name(i[0])}. \nСдать до: {(await get_date(i[0]) + datetime.timedelta(days=7)).strftime("%d/%m/%y")}')
    await message.answer('\n\n'.join(str_books))
    await log_add(message.from_user.id, 'Мои книги', datetime.datetime.now(), f"books = {', '.join(str_books)}")