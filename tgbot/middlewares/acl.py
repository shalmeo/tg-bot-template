from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.database.models import User
from tgbot.services.database.quick_commands import fetch_user




class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, tg_user: types.User):
        session: AsyncSession = data['session']
        user = await fetch_user(session, tg_user.id)
        if user is None:
            await session.merge(User(user_id=tg_user.id, 
                                     full_name=tg_user.full_name))
            await session.commit()
            user = User(user_id=tg_user.id, 
                        full_name=tg_user.full_name)
        data['user'] = user
        
        

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.setup_chat(data, call.from_user)