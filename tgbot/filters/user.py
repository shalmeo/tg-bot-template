from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.config import Config


class UserFilter(BoundFilter):
    key = 'is_user'
    is_user: bool
    
    def __init__(self, is_user):
        self.is_user = is_user

    async def check(self, message: types.Message):
        data = ctx_data.get()
        config: Config = data['config']
        return message.from_user.id not in config.tg_bot.admin_ids