import os
import logging
import sys
from dotenv import load_dotenv
import aiohttp
import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


dotenv_path = os.path.join(
    '..',
    '.env'
)
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('TOKEN')

dp = Dispatcher()
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Ответ на сообщение /start

    Args:
        message (Message): _description_
    """    
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}!')


@dp.message()
async def echo_handler(message: Message) -> None:
    """Ответ на сообщение от пользователя

    Args:
        message (Message): _description_
    """   
    # отправляем в ответ сообщение пользователя 
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

    # Генерация ссылки на фото, если оно есть в сообщении
    if message.photo is not None:
        file_info = await bot.get_file(message.photo[-1].file_id)
        print('url', f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')

    # Тест
    # Отправка задачи на отправку сообщения
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url='http://127.0.0.1:8000/send/',
            json={
                'chat_id': message.chat.id,
                'text': 'Here will be game history',
                'reply_to_msg_id': message.message_id
            }
        )
        print(await response.json())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
