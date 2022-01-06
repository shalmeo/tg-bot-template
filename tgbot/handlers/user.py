from aiogram import Dispatcher
from aiogram.types import Message


@rate_limit(5, key='start')
async def user_start(message: Message):
    await message.reply("Hello, user!")


def setup(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
