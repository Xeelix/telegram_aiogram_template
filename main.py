import logging

import asyncio
import os
import sys

import colorama as colorama
from aiogram import Bot, Dispatcher

from tgbot.data.config import BOT_TOKEN, get_admins
from tgbot.utils.misc.bot_logging import bot_logger
from tgbot.routers import register_all_routers
from tgbot.services.api_session import AsyncRequestSession
from tgbot.utils.misc.bot_commands import set_commands
from tgbot.utils.misc_functions import startup_notify


async def main():
    dp = Dispatcher()
    arSession = AsyncRequestSession()  # Пул асинхронной сессии запросов
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")  # Образ Бота

    register_all_routers(dp)  # Регистрация всех роутеров

    try:
        await set_commands(bot)

        await startup_notify(bot, arSession)

        bot_logger.warning("BOT WAS STARTED")
        print(colorama.Fore.LIGHTYELLOW_EX + f"~~~~~ Bot was started - @{(await bot.get_me()).username} ~~~~~")
        print(colorama.Fore.RESET)

        if len(get_admins()) == 0: print("***** ENTER ADMIN ID IN settings.ini *****")

        await bot.delete_webhook()
        await bot.get_updates(offset=-1)

        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            arSession=arSession,
        )
    finally:
        await arSession.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        bot_logger.warning("Bot was stopped")
    finally:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")