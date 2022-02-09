from aiogram import Dispatcher, types


async def start(message: types.Message):
    await message.answer('Hello user')


def setup(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state='*')