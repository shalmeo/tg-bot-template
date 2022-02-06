from aiogram import types, Dispatcher


async def plug(message: types.Message):
    pass
    
    
def setup(dp: Dispatcher):
    dp.register_message_handler(plug)