from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from .get_info import admin
from bot.commands.profile import new_user


 # Создает меню
async def start(message: types.Message) -> None:
    await message.answer('✋Привет. Добро пожаловать в библиотеку ШТД')

    menu_builder = ReplyKeyboardBuilder()
    menu_builder.row(KeyboardButton(text="📚Книги списком"), KeyboardButton(text="Книги по ключевому слову"))
    menu_builder.row(KeyboardButton(text='ℹ️Профиль'), KeyboardButton(text="Мои книги"))
    menu_builder.add(KeyboardButton(text="💬 Помощь"))
    if await admin(message.from_user.id):
        menu_builder.add(KeyboardButton(text="📖Добавить физ. книгу"))
        # menu_builder.add(KeyboardButton(text="📁Добавить электр. книгу")) # TODO
    else: print('no admin', message.from_user.id)
    await new_user(message)
    await message.answer('🔮Главное меню', reply_markup=menu_builder.as_markup(), resize=True)