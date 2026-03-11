import os
from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI

from schemas.tg_send_message import SendMsgTask

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.reply_parameters import ReplyParameters



dotenv_path = os.path.join(
    '..',
    '.env'
)
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('TOKEN')

app = FastAPI()
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

@app.post("/send/")
async def send_message(task: SendMsgTask):
    async with bot:
        reply_params = ReplyParameters(
            message_id=task.reply_to_msg_id
        )
        await bot.send_message(
            chat_id=task.chat_id,
            text=task.text,
            reply_parameters=reply_params
        )
