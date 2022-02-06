import re

from typing import Union
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.reply import menu_kb
from tgbot.misc.allow_acc import allow_acces
from tgbot.misc.referal import add_referal
from tgbot.keyboards.inline import starting_kb
from tgbot.services.database.models import User


async def start_for_new(obj: Union[types.Message, types.CallbackQuery]):
    send_message = obj.message.edit_text if isinstance(obj, types.CallbackQuery) else obj.answer
    
    await send_message("Привет 👋\n"
                       "Чтобы пользоваться ботом 🤖, тебе нужно выполнить один из этих пунктов:\n\n"
                       "📍 Быть подписанным на наш новостной канал\n"
                       "📍 Быть приглашенным от кого-либо\n"
                       "📍 Ввести код пригасившего", reply_markup=starting_kb())


async def user_start(message: types.Message):
    await message.answer('Вы были перенесены в меню! 🎛', reply_markup=menu_kb())
    

@allow_acces()
async def user_start_with_deeplink(message: types.Message, session: AsyncSession, user: User):
    ref_id = int(message.get_args())
    result = await session.execute(select(User).where(User.user_id==ref_id))
    ref: User = result.scalars().first()
    
    if ref:
        await message.answer('Вы были перенесены в меню! 🎛', reply_markup=menu_kb())
        await add_referal(session=session, ref=ref, user=user)
    else:
        await start_for_new(message)
    

def setup(dp: Dispatcher):
    dp.register_message_handler(user_start_with_deeplink, CommandStart(deep_link=re.compile(r'^\d{1,}$')), 
                                                          state='*', is_user=True)
    dp.register_message_handler(user_start, commands=["start"], state='*')