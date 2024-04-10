from engine import *
from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_datafactory import EditBookCallbackData
from .get_info import get_book_name, admin, log_add, get_student_info, get_group_by_book, get_date, get_storage
from aiogram.types import FSInputFile
import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

show_books_router = Router()

class Search_Tags(StatesGroup):
    Search = State()

# создает список книг и кнопки для их выбора
async def books_show_list(message: types.Message):
    buttons = InlineKeyboardBuilder()
    cur.execute('SELECT book_id from books')
    books_id = cur.fetchall()
    list_books = []
    for id in range(1, len(books_id)+1):
        emoji = ['✅', '❌', '🌐']
        cur.execute(f"select holder from books where book_id={books_id[id-1][0]}")
        holder_status = cur.fetchone()[0]
        if holder_status == '0':
            emoji = emoji[0]
        elif holder_status == 'E':
            emoji = emoji[2]
        else:
            emoji = emoji[1]
        list_books.append(f'{id}. {await get_book_name(books_id[id-1][0])} {emoji}')
        buttons.button(text=str(id), callback_data=EditBookCallbackData(command='show_book', book_id=str(books_id[id-1][0]), user_id=f'{message.from_user.id}', group_name=''))
    text_books = '\n'.join(list_books)
    await message.answer(f'{text_books}')
    await message.answer('Книги', reply_markup=buttons.as_markup(resize_keyboard=True))
    await log_add(message.from_user.id, 'Книги списком', datetime.datetime.now())

# даёт информацию о книге и позволяет изменить хранилище и держателя админу
async def book_info(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    cur.execute(f'select link from books where book_id = {int(callback_data.book_id)}')
    buttons_to_edit = InlineKeyboardBuilder()
    E = False
    # Проверка электронная ли книга
    if cur.fetchone()[0] != 'None':
        E = True
        buttons_to_edit.button(text='Скачать', callback_data=EditBookCallbackData(command='download_book', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=''))
    # Проверка есть ли права на редактирование книги
    if await admin(callback_data.user_id):
        if not E:
            buttons_to_edit.button(text='Поменять держателя', callback_data=EditBookCallbackData(command='choose_group_from_list', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=''))
            buttons_to_edit.button(text='Поменять хранилище', callback_data=EditBookCallbackData(command='ask_for_storage', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=''))
        buttons_to_edit.button(text='Удалить книгу', callback_data=EditBookCallbackData(command='ask_for_delete_book', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=''))
        buttons_to_edit.button(text='Установить теги', callback_data=EditBookCallbackData(command='ask_tags', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=''))
        buttons_to_edit.button(text='Получить теги', callback_data=EditBookCallbackData(command='get_tags', book_id=str(callback_data.book_id), user_id=callback_data.user_id, group_name=''))
    if E:
        await call.message.answer(f'"{await get_book_name(callback_data.book_id)}"', reply_markup=buttons_to_edit.as_markup())
        return
    if type(call) != types.Message:
        await call.message.answer(f'''Информация о книге \n"{await get_book_name(callback_data.book_id)}":\n
    Держатель: "{await get_student_info(callback_data.book_id)} {await get_group_by_book(callback_data.book_id)}"\n
    Должен вернуть по {(await get_date(callback_data.book_id) + datetime.timedelta(days=7)).strftime("%d/%m/%y")}\n
    Хранилище: "{await get_storage(callback_data.book_id)}"''', reply_markup=buttons_to_edit.as_markup())
    else:
        await call.answer(f'''Информация о книге \n"{await get_book_name(callback_data.book_id)}":\n
    Держатель: "{await get_student_info(callback_data.book_id)} {await get_group_by_book(callback_data.book_id)}"\n
    Должен вернуть по {(await get_date(callback_data.book_id) + datetime.timedelta(days=7)).strftime("%d/%m/%y")}\n
    Хранилище: "{await get_storage(callback_data.book_id)}"''', reply_markup=buttons_to_edit.as_markup())


async def download_book(call: types.callback_query, callback_data: EditBookCallbackData):
    cur.execute(f"select link from books where name='{await get_book_name(callback_data.book_id)}'")
    link = cur.fetchone()[0]
    await call.message.answer(link)
    await log_add(callback_data.user_id, 'Скачать книгу', datetime.datetime.now(), f"book = {await get_book_name(callback_data.book_id)}")

async def ask_tag_search(message: types.Message, state: FSMContext):
    await message.answer('Введите тег, по которому хотите найти книгу')
    await state.set_state(Search_Tags.Search)

@show_books_router.message(Search_Tags.Search)
async def choose_tags(message: types.Message, state: FSMContext):
    search_tag = message.text.lower().replace('#', '')
    buttons = InlineKeyboardBuilder()
    cur.execute(f"select text from tags")
    list_tags = []
    tags = sorted([x[0].lower() for x in cur.fetchall()])
    for id in range(len(tags)):
        if search_tag not in tags[id]:
            continue
        if len(search_tag) < 2:
            continue
        list_tags.append(f'#{len(list_tags)+1}. {tags[id]}')
        cur.execute(f"select books from tags where text='{tags[id]}'")
        buttons.button(text=str(len(list_tags)), callback_data=EditBookCallbackData(command='search_tag', book_id=f'{cur.fetchone()[0]}', user_id=f'{message.from_user.id}', group_name=''))
    text_tags = '\n\n'.join(list_tags)
    if len(text_tags) == 0: 
        await message.answer(f'Тег не найден')
        await state.clear()
        await log_add(message.from_user.id, 'Поиск по тегу', datetime.datetime.now(), f"No tags")
        return
    await message.answer(f'{text_tags}')
    await message.answer('Выберите тег из списка', reply_markup=buttons.as_markup(resize_keyboard=True))
    await state.clear()
    text_tags = text_tags.replace('\n', ' ')
    await log_add(message.from_user.id, 'Поиск по тегу', datetime.datetime.now(), f"tag = {search_tag}; founded_tags = {text_tags}")

async def show_books_tags(call: types.CallbackQuery, callback_data: EditBookCallbackData):
    buttons = InlineKeyboardBuilder()
    books = str(callback_data.book_id.split(';'))[1:-1]
    cur.execute(f'SELECT book_id from books where book_id in ({books})')
    books_id = cur.fetchall()
    list_books = []
    for id in range(len(books_id)):
        emoji = ['✅', '❌', '🌐']
        cur.execute(f"select holder from books where book_id={books_id[id][0]}")
        holder_status = cur.fetchone()[0]
        if holder_status == '0':
            emoji = emoji[0]
        elif holder_status == 'E':
            emoji = emoji[2]
        else:
            emoji = emoji[1]
        list_books.append(f'{id}. {await get_book_name(books_id[id][0])} {emoji}')
        buttons.button(text=str(id), callback_data=EditBookCallbackData(command='show_book', book_id=str(books_id[id][0]), user_id=f'{callback_data.user_id}', group_name=''))
    text_books = '\n\n'.join(list_books)
    await call.message.answer(f'{text_books}')
    await call.message.answer('Книги', reply_markup=buttons.as_markup(resize_keyboard=True))