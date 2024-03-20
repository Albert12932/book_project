import asyncio
import logging
from config import TOKEN
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from bot.commands.__init__ import register_user_commands
from bot.commands.tables_create import create_tables, update_books
from bot.commands.bot_commands import bot_commands
from bot.commands.edit_books import edit_books_router
from bot.commands.add_book import add_book_router
from bot.commands.profile import add_info_router
from bot.commands.show_books import show_books_router
# Регистрация бота, диспатчера, роутеров
async def main() -> None:

    logging.basicConfig(level=logging.DEBUG)

    dp = Dispatcher()
    
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    # dp.include_router(register_router)
    dp.include_router(edit_books_router)
    dp.include_router(add_book_router)
    dp.include_router(add_info_router)
    dp.include_router(show_books_router)
    bot = Bot(TOKEN)

    await bot.set_my_commands(commands=commands_for_bot)
    create_tables()
    await update_books()
    register_user_commands(dp)

    await dp.start_polling(bot)

# Запуск
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
