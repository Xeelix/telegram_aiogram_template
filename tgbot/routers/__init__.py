from aiogram import Dispatcher, F

from tgbot.routers import main_start


def register_all_routers(dp: Dispatcher):
    dp.message.filter(F.chat.type == "private")  # Работа бота только в личке - сообщения
    dp.callback_query.filter(F.message.chat.type == "private")  # Работа бота только в личке - колбэки



    # Подключение обязательных роутеров
    dp.include_router(main_start.router)  # Роутер основных команд

