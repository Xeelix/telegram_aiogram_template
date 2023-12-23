# - *- coding: utf- 8 - *-
import asyncio
import json
from typing import Union

from aiogram import Bot
from aiogram.types import FSInputFile

from tgbot.data.config import get_admins, BOT_VERSION, PATH_DATABASE, get_desc
from tgbot.utils.const_functions import get_unix, get_date, ded, send_admins
from tgbot.utils.misc.bot_models import ARS


# Уведомление и проверка обновления при запуске бота
async def startup_notify(bot: Bot, arSession: ARS):
    if len(get_admins()) >= 1:
        await send_admins(
            bot,
            ded(f"""
                <b>✅ Бот успешно запущен</b>
                ➖➖➖➖➖➖➖➖➖➖
                <code>❗ Данное сообщение видят только администраторы бота.</code>
            """),
        )



# Автобэкапы БД для админов
async def autobackup_admin(bot: Bot):
    for admin in get_admins():
        try:
            await bot.send_document(
                admin,
                FSInputFile(PATH_DATABASE),
                caption=f"<b>📦 #BACKUP | <code>{get_date(full=False)}</code></b>",
                disable_notification=True,
            )
        except:
            ...



# Загрузка текста на текстовый хостинг
async def upload_text(arSession: ARS, text: str) -> str:
    session = await arSession.get_session()

    spare_pass = False
    await asyncio.sleep(0.5)

    try:
        response = await session.post(
            "http://pastie.org/pastes/create",
            data={'language': 'plaintext', 'content': text},
        )

        get_link = response.url
        if "create" in str(get_link): spare_pass = True
    except:
        spare_pass = True

    if spare_pass:
        response = await session.post(
            "https://www.friendpaste.com",
            json={'language': 'text', 'title': '', 'snippet': text},
        )

        get_link = json.loads((await response.read()).decode())['url']

    return get_link


# Загрузка изображения на хостинг телеграфа
async def upload_photo(arSession: ARS, this_photo) -> str:
    session = await arSession.get_session()

    send_data = {
        'name': 'file',
        'value': this_photo,
    }

    async with session.post("https://telegra.ph/upload", data=send_data, ssl=False) as response:
        img_src = await response.json()

    return "http://telegra.ph" + img_src[0]['src']
