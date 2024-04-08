from engine import *
from aiogram import types, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from .get_info import admin, log_add
import os
import datetime


add_book_router = Router()

class add_book(StatesGroup):
    phys_book_add = State()
    file_download = State()

async def phys_book_name_wait(message: types.Message, state: FSMContext):
    if not await admin(message.from_user.id):
        await message.answer('Вы не администратор')
        return
    await message.answer('Введите название книги')
    await state.set_state(add_book.phys_book_add)
    

@add_book_router.message(add_book.phys_book_add)
async def phys_book_add(message: types.Message, state: FSMContext):
    cur.execute(f"insert into books (name) values ('{message.text}')")
    conn.commit()
    await message.answer(f'Книга <{message.text}> успешно добавлена')
    await state.clear()
    await log_add(str(message.from_user.id), 'Добавить физ. книгу', datetime.datetime.now(), f'{message.text}')


# @add_book_router.message(add_book.file_download)
# async def download_file(message: types.Message, state: FSMContext, bot: Bot):
#     file_id = message.document.file_id
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     await bot.download_file(file_path, 'text.txt')
#     await state.clear_state()