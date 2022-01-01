from aiogram import types
from aiogram import Dispatcher


async def set_dafault_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт')
    ])