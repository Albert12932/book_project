__all__ = ['register_user_commands', 'bot_commands']

from engine import *
from aiogram import Router, F
from aiogram.filters import Command
from .show_books import book_info, books_show_list, download_book, ask_tag_search, show_books_tags
from .callback_datafactory import EditBookCallbackData
from .edit_books import *
from .add_book import *
from .start import start
from .profile import profile_show, add_info, help, my_books
from .tables_create import *


def register_user_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.message.register(profile_show, F.text=='ℹ️Профиль')
    router.callback_query.register(add_info, EditBookCallbackData.filter(F.command=='add_info'))
    router.message.register(books_show_list, F.text=='📚Книги списком')
    router.message.register(ask_tag_search, F.text=='Книги по ключевому слову')
    router.callback_query.register(show_books_tags, EditBookCallbackData.filter(F.command=='search_tag'))
    router.message.register(my_books, F.text=='Мои книги')
    router.message.register(books_show_list, Command(commands=['books']))
    router.callback_query.register(download_book, EditBookCallbackData.filter(F.command=='download_book'))
    router.callback_query.register(book_info, EditBookCallbackData.filter(F.command=='show_book'))
    router.callback_query.register(choose_holder_from_list, EditBookCallbackData.filter(F.command=='choose_holder'))
    router.callback_query.register(edit_holder, EditBookCallbackData.filter(F.command=='edit_holder'))
    router.callback_query.register(remove_holder, EditBookCallbackData.filter(F.command=='remove_holder'))
    router.callback_query.register(ask_for_delete_book, EditBookCallbackData.filter(F.command=='ask_for_delete_book'))
    router.callback_query.register(delete_book, EditBookCallbackData.filter(F.command=='delete_book'))
    router.callback_query.register(choose_group_from_list, EditBookCallbackData.filter(F.command=='choose_group_from_list'))
    router.callback_query.register(ask_for_storage, EditBookCallbackData.filter(F.command=='ask_for_storage'))
    router.callback_query.register(ask_tags, EditBookCallbackData.filter(F.command=='ask_tags'))
    router.callback_query.register(set_tag, EditBookCallbackData.filter(F.command=='set_tag'))
    router.callback_query.register(get_tags, EditBookCallbackData.filter(F.command=='get_tags'))


    router.message.register(phys_book_name_wait, F.text=='📖Добавить физ. книгу')
    router.message.register(help, F.text=='💬 Помощь')
    
    # router.message.register(net_book_file_wait, F.text=='📁Добавить электр. книгу')  # TODO
    
    
    
    

    
    

    

    