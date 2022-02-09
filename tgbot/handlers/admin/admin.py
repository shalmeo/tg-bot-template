from aiogram import types, Dispatcher

async def admin(message: types.Message):
    await message.answer('Hello admin')

def setup(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['start'], state='*', is_admin=True)