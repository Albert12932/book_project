from engine import *
from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import callback_query
from .callback_datafactory import EditBookCallbackData
from .get_info import log_add, get_book_name, get_id_by_surname
from .show_books import book_info
import datetime


edit_books_router = Router()

class EditBooks(StatesGroup):
    edit_holder = State()
    edit_storage = State()
    add_book = State()

class Tags(StatesGroup):
    set_tags = State()

# запрашивает хранилище книги
async def ask_for_storage(call:callback_query, state: FSMContext):
    await call.message.answer('Введите хранилище')
    await state.set_state(EditBooks.edit_storage)
    await state.update_data(info=call.data.split(':'))

# меняет хранилище книги
@edit_books_router.message(EditBooks.edit_storage)
async def edit_storage(message: types.Message, state: FSMContext):

    new_storage = message.text
    data = await state.get_data()
    book_id = data['info'][2]
    userid = data['info'][3]
    cur.execute(f"update books set storage = '{new_storage}' where book_id = {book_id}")
    conn.commit()

    await book_info(message, callback_data=EditBookCallbackData(command='', book_id=str(book_id), group_name='', user_id=userid))
    await state.clear()
    await log_add(str(message.from_user.id), 'Изменить хранилище', datetime.datetime.now(), f'new_storage = {new_storage};book = {await get_book_name(book_id)}')

async def choose_group_from_list(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    cur.execute('select distinct group_name from people')
    groups = []
    group_buttons = InlineKeyboardBuilder()
    groups_names = cur.fetchall()
    group_buttons.button(text='Никто', callback_data=EditBookCallbackData(command='remove_holder', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=f'{callback_data.group_name}'))
    for i in range(len(groups_names)):
        groups.append(groups_names[i][0])
    for group in groups:
        group_buttons.button(text=f'{group}', callback_data=EditBookCallbackData(command='choose_holder', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=f'{group}'))
    await call.message.answer('Выберите группу', reply_markup=group_buttons.as_markup())

async def choose_holder_from_list(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    cur.execute(f"select surname from people where group_name = '{callback_data.group_name}'")
    holders = []
    holder_buttons = InlineKeyboardBuilder()
    holders_names = cur.fetchall()
    for i in range(len(holders_names)):
        holders.append(holders_names[i][0])
    for holder_surname in holders:
        holder_buttons.button(text=f'{holder_surname}', callback_data=EditBookCallbackData(command='edit_holder', book_id=str(callback_data.book_id), group_name=callback_data.group_name, user_id=await get_id_by_surname(holder_surname)))
    await call.message.answer('Выберите держателя', reply_markup=holder_buttons.as_markup())

async def edit_holder(message: types.Message, callback_data: EditBookCallbackData):
    cur.execute(f"update books set holder = '{callback_data.user_id}' where book_id = {int(callback_data.book_id)}")
    cur.execute(f"update books set date_taken = '{datetime.datetime.today()}' where book_id = {int(callback_data.book_id)}")
    conn.commit()
    await book_info(message, callback_data=EditBookCallbackData(command='', book_id=callback_data.book_id, group_name='', user_id=str(message.from_user.id)))
    await log_add(str(message.from_user.id), 'Изменить держателя', datetime.datetime.now(), f'user_id = {callback_data.user_id};book = {await get_book_name(callback_data.book_id)}')

async def ask_tags(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Введите теги в формате: Тег1#Тег2#Тег3#Тег4')
    await state.set_state(Tags.set_tags)
    await state.update_data(book_id=call.data.split(':'))

@edit_books_router.message(Tags.set_tags)
async def set_tag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    book_id = data['book_id'][2]
    text = message.text.replace(' ', '').replace('\n', '')
    cur.execute(f"update books set book_tags = '{text}' where book_id = {book_id}")
    conn.commit()
    cur.execute(f"select text from tags")
    tags = [x[0].lower() for x in cur.fetchall()]
    for tag in text[1:].split('#'):
        if tag.lower() in tags:
            cur.execute(f"select books from tags where text = '{tag.lower()}'")
            result = cur.fetchone()[0].split(';')
            result.append(book_id)
            cur.execute(f"update tags set books = '{';'.join(result)}' where text= '{tag.lower()}'")
        else:
            cur.execute(f"insert into tags (text, books) values ('{tag.lower()}', '{book_id}')")
    await message.answer(f'Теги успешно установлены')
    await state.clear()
    await log_add(message.from_user.id, 'Установить теги', datetime.datetime.now(), f'book = {await get_book_name(book_id)};tags = {text.lower()}')
    conn.commit()

async def get_tags(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    cur.execute(f"select book_tags from books where book_id = {callback_data.book_id}")
    tags = [x[0] for x in cur.fetchall()]
    if tags == [None]:
        await call.message.answer('У данной книги нет тегов')
        tags = ''
        await log_add(callback_data.user_id, 'Получить теги', datetime.datetime.now(), f"book = {await get_book_name(callback_data.book_id)}; Нет тегов. tags = {'#'.join(tags)}")
        return
    await call.message.answer('#'.join(tags))
    await log_add(callback_data.user_id, 'Получить теги', datetime.datetime.now(), f"book = {await get_book_name(callback_data.book_id)};tags = {'#'.join(tags)}")

async def ask_for_delete_book(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    del_button = InlineKeyboardBuilder()
    del_button.button(text='Да', callback_data=EditBookCallbackData(command='delete_book', book_id=callback_data.book_id, user_id=callback_data.user_id, group_name=''))
    del_button.button(text='Нет', callback_data=EditBookCallbackData(command='', book_id=callback_data.book_id, user_id=callback_data.user_id, group_name=''))
    await call.message.answer(f'Вы уверены, что хотите удалить книгу <{await get_book_name(callback_data.book_id)}>', reply_markup=del_button.as_markup())

async def delete_book(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    await call.message.answer(f'Книга <{callback_data.book_id}> успешно удалена')
    await log_add(call.message.from_user.id, 'Удалить книгу', datetime.datetime.now(), f'book = {await get_book_name(callback_data.book_id)}')
    cur.execute(f'delete from books where book_id = {callback_data.book_id}')
    conn.commit()

async def remove_holder(call: types.CallbackQuery, callback_data:EditBookCallbackData):
    cur.execute(f"update books set holder = '0' where book_id = {callback_data.book_id}")
    conn.commit()
    await book_info(call.message, callback_data=EditBookCallbackData(command='', book_id=callback_data.book_id, group_name='', user_id=callback_data.user_id))
    await log_add((callback_data.user_id), 'Удалить держателя', datetime.datetime.now(), f'user_id = {callback_data.user_id};book = {await get_book_name(callback_data.book_id)}')