from aiogram import Dispatcher
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.database.models import User
from tgbot.misc.throttling import rate_limit


@rate_limit(5, key='start')
async def user_start(message: Message, session: AsyncSession):
    await message.reply("Hello, user!")
    
    await session.merge(User(user_id=message.from_user.id, allow=False))
    await session.commit()


def setup(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")