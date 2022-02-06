from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from tgbot.services.database.models import User
from tgbot.services.database.quick_commands import fetch_user


async def add_referal(session: AsyncSession, ref: User, user: User):
    ref: User = await fetch_user(session, ref.user_id)
    
    if user.user_id not in ref.referals:
        ref.referals = list(ref.referals)
        ref.referals.append(user.user_id)
        ref.points += 10

    
    if not user.referal:
        user.referal = ref.user_id
    
    await session.commit()