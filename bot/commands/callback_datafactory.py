from aiogram.filters.callback_data import CallbackData

class EditBookCallbackData(CallbackData, prefix="eb"):
    command: str
    book_id: str
    user_id: str
    group_name: str