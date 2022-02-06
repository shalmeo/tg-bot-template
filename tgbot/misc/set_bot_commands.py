from aiogram import types
from aiogram import Bot


async def set_dafault_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand('start', 'Старт')
    ])