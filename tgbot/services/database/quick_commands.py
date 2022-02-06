from asyncio.log import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from tgbot.services.database.models import Items, User


async def fetch_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
   
    return user


async def fetch_item(session: AsyncSession, item_id: int):
    item = await session.get(Items, item_id)
    
    return item

async def merge_item(session: AsyncSession, **kwargs):
    try:
        await session.merge(Items(**kwargs))
        await session.commit()
        return True
    except Exception as err:
        logger.info(err)
        return


async def delete_item(session: AsyncSession, item_id):
    try:
        await session.execute(delete(Items).where(Items.id==item_id))
        await session.commit()
        return True
    except Exception as err:
        logger.info(err)
        return